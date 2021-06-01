import logging as logger
from flask import Flask, request
from haystack.document_store.elasticsearch import ElasticsearchDocumentStore

from haystack.pipeline import ExtractiveQAPipeline, Pipeline, JoinDocuments
from haystack.reader.farm import FARMReader
from haystack.retriever.dense import DensePassageRetriever
from haystack.retriever.sparse import ElasticsearchRetriever


logger.basicConfig(level="INFO")
app = Flask(__name__)

logger.info("Loading restapi.")
document_store = ElasticsearchDocumentStore(host="localhost", username="", password="", index="amitblogs")

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


logger.info("Initialization of reader.")
reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=False)

logger.info("Runnning query classifier")
class QueryClassifier():
    outgoing_edges = 2

    def run(self, **kwargs):
        if "?" in kwargs["query"]:
            return (kwargs, "output_2")
        else:
logger.info("Building pipeline.")

# p = Pipeline()
# p.add_node(component=es_retriever, name="ESRetriever", inputs=["Query"])
# p.add_node(component=dpr_retriever, name="DPRRetriever", inputs=["Query"])
# p.add_node(component=JoinDocuments(join_mode="concatenate"), name="JoinResults", inputs=["ESRetriever", "DPRRetriever"])
# p.add_node(component=reader, name="Reader", inputs=["JoinResults"])

p_classifier = Pipeline()
p_classifier.add_node(component=QueryClassifier(), name="QueryClassifier", inputs=["Query"])
p_classifier.add_node(component=es_retriever, name="ESRetriever", inputs=["QueryClassifier.output_1"])
p_classifier.add_node(component=dpr_retriever, name="DPRRetriever", inputs=["QueryClassifier.output_2"])
p_classifier.add_node(component=reader, name="QAReader", inputs=["ESRetriever", "DPRRetriever"])


logger.info("Building pipeline.")

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
        response = p_classifier.run(query=data['questions'], top_k_retriever=10)
        print(response)
        logger.info("processing completed")
        return response
    else:
        return 400
    


if __name__ == '__main__':
    logger.info("Starting the application")
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)
