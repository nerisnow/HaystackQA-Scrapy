import logging as logger
from flask import Flask, request
from haystack.document_store.elasticsearch import ElasticsearchDocumentStore

from haystack.retriever.dense import DensePassageRetriever
from haystack.pipeline import ExtractiveQAPipeline
from haystack.reader.farm import FARMReader

logger.basicConfig(level="INFO")
app = Flask(__name__)

logger.info("Loading restapi.")
document_store = ElasticsearchDocumentStore(host="localhost", username="", password="", index="document")

logger.info("Initialization Of ES Retriever.")
es_retriever = ElasticsearchRetriever(document_store=document_store)

logger.info("Initialization Of DPR.")
dpr_retriever = DensePassageRetriever(document_store=document_store,
                                  query_embedding_model="facebook/dpr-question_encoder-single-nq-base",
                                  passage_embedding_model="facebook/dpr-ctx_encoder-single-nq-base",
                                  max_seq_len_query=64,
                                  max_seq_len_passage=256,
                                  batch_size=16,
                                  use_gpu=True,
                                  embed_title=True,
                                  use_fast_tokenizers=True)

# document_store.update_embeddings(retriever)

logger.info("Initialization of reader.")
reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=False)

logger.info("Building pipeline.")
# pipe = ExtractiveQAPipeline(reader, retriever)

p = Pipeline()
p.add_node(component=es_retriever, name="ESRetriever1", inputs=["Query"])
p.add_node(component=dpr_retriever, name="DPRRetriever1", inputs=["Query"])
p.add_node(component=JoinDocuments(join_mode="concatenate"), name="JoinResults", inputs=["ESRetriever1", "DPRRetriever1"])
p.add_node(component=reader, name="Reader", inputs=["JoinResults"])

@app.route('/', methods=["GET"])
def health():
    logger.info("Checking health")
    return str(200)

@app.route('/predict', methods=["POST"])
def predict():
    logger.info("Received question")
    logger.info("processing question")
    data = request.get_json()
    if data['questions'] is not None:
        response = pipe.run(query=data['questions'], top_k_retriever=10, top_k_reader=5)
        print(response)
        logger.info("processing completed")
        return response
    else:
        return 400
    


if __name__ == '__main__':
    logger.info("Starting the application")
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)
