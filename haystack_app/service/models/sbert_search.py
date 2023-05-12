from haystack.utils import launch_es
import os
from haystack.document_stores import ElasticsearchDocumentStore

print("start")
launch_es()
print("launch_es")

print("start")
# Elasticsearch로 문서 저장소 설정
host = os.environ.get("ELASTICSEARCH_HOST", "localhost")

document_store = ElasticsearchDocumentStore(
    host=host,
    username="",
    password="",
    index="document"
)
print("ElasticsearchDocumentStore")






