import os
from haystack.document_stores import ElasticsearchDocumentStore
from haystack.nodes import BM25Retriever, DensePassageRetriever
from haystack.pipelines import DocumentSearchPipeline
from haystack.utils import convert_files_to_docs, launch_es
import logging


logging.basicConfig(
    format="%(levelname)s - %(name)s -  %(message)s", level=logging.WARNING
)
logging.getLogger("haystack").setLevel(logging.INFO)


# 지정한 위치에 있는 데이터를 받아옴
print("now dir ls = ", os.listdir("."))
doc_dir = "service/law_data"


launch_es()

# Elasticsearch를 document_store에 연결 > fault_rate_bm25_search
document_store = ElasticsearchDocumentStore(
    host="elasticsearch_for_haystack_app",  # local 환경 에서는 "localhost"
    username="",
    password="",
    index="fault_rate_bm25_search",  # 인덱스 설정
)
