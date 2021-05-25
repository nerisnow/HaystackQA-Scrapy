import logging as logger
from zipfile import ZipFile
from haystack.preprocessor.cleaning import clean_wiki_text
from haystack.preprocessor.utils import convert_files_to_dicts
from haystack.document_store.elasticsearch import ElasticsearchDocumentStore
from haystack.retriever.dense import DensePassageRetriever

logger.basicConfig(level="INFO")

# file_name = "data2.zip"
  
# opening the zip file in READ mode
# with ZipFile(file_name, 'r') as zip:
#     # printing all the contents of the zip file
#     zip.printdir()
  
#     # extracting all the files
#     logger.info('Extracting all the files now...')
#     zip.extractall()
#     logger.info("Completed Extracting")



#path for the data files
doc_dir = "data"

#instance for document store
document_store = ElasticsearchDocumentStore(
    host="localhost", username="", password="", 
    index="amitblogs")

# Convert files to dicts
dicts = convert_files_to_dicts(dir_path=doc_dir,clean_func=clean_wiki_text,split_paragraphs=True)

# write the dicts containing documents to our DB.
document_store.write_documents(dicts)
logger.info("Completed writing")
logger.info("Loading Retriever.")

#create retriever
retriever = DensePassageRetriever(document_store=document_store,
                                  query_embedding_model="facebook/dpr-question_encoder-single-nq-base",
                                  passage_embedding_model="facebook/dpr-ctx_encoder-single-nq-base",
                                  max_seq_len_query=64,
                                  max_seq_len_passage=256,
                                  batch_size=16,
                                  use_gpu=True,
                                  embed_title=True,
                                  use_fast_tokenizers=True)
logger.info("updating embedding.")
document_store.update_embeddings(retriever)
logger.info("Completed loading embedding.")
logger.info("Compled Indexing")
