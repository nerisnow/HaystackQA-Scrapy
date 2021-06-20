import json
import json_lines

import logging as logger
from zipfile import ZipFile
from haystack.preprocessor.cleaning import clean_wiki_text
from haystack.preprocessor.utils import fetch_archive_from_http, convert_files_to_dicts
from haystack.document_store.elasticsearch import ElasticsearchDocumentStore
from haystack.retriever.dense import DensePassageRetriever


logger.basicConfig(level="INFO")

# path for the .txt data files
local_doc_dir = "/content/HaystackQA-Scrapy/amitness/data"

# instance for document store
document_store = ElasticsearchDocumentStore(
    host="localhost", username="", password="", index="amitblogs"
)

# clearing any previously indexed documents
document_store.delete_all_documents()


## download and prepare scraped data
# s3 instance api
s3_url = ""

# directory to store fetched s3 data
output_dir = ""

# fetch_archive_from_http(url=s3_url, output_dir=output_dir)

# Convert files to dicts
# dicts = convert_files_to_dicts(
#     dir_path=output_dir,
#     clean_func=clean_wiki_text,
#     split_paragraphs=True)

filename = "/content/HaystackQA-Scrapy/amitness/blogs.json"
list_of_dict = []

with open(filename, "rb") as f:
    for item in json_lines.reader(f):
        list_of_dict.append(item)

# write the dicts containing documents to our DS.
document_store.write_documents(list_of_dict)
logger.info("Completed writing")

logger.info("Loading Retriever.")
# create retriever
retriever = DensePassageRetriever(
    document_store=document_store,
    query_embedding_model="facebook/dpr-question_encoder-single-nq-base",
    passage_embedding_model="facebook/dpr-ctx_encoder-single-nq-base",
    max_seq_len_query=64,
    max_seq_len_passage=256,
    batch_size=16,
    use_gpu=True,
    embed_title=True,
    use_fast_tokenizers=True,
)
logger.info("updating embedding.")
document_store.update_embeddings(retriever)
logger.info("Completed loading embedding.")
logger.info("Compled Indexing")
