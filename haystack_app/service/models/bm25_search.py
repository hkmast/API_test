import os
from haystack.document_stores import ElasticsearchDocumentStore
from haystack.nodes import BM25Retriever
from haystack.pipelines import DocumentSearchPipeline
from haystack.utils import convert_files_to_docs

# 지정한 위치에 있는 데이터를 받아옴
print("now dir ls = ", os.listdir("."))
doc_dir = "./haystack_app/law_data"

# Elasticsearch를 document_store에 연결
document_store = ElasticsearchDocumentStore(
    host="elasticsearch_for_haystack_app",  # local 환경 에서는 "localhost"
    username="",
    password="",
    index="bm25_search",  # 인덱스 설정
)

# 파일들을 딕셔너리 형태로 변환하여 색인
docs = convert_files_to_docs(dir_path=doc_dir, clean_func=None)
document_store.write_documents(docs)

# BM25 Retriever 설정
retriever = BM25Retriever(document_store=document_store)

# Document Search Pipeline 설정
pipeline = DocumentSearchPipeline(retriever)


# 검색 함수
def search(query, k):
    return pipeline.run(query, params={"Retriever": {"top_k": int(k)}})


# 테스트
if __name__ == "__main__":
    print(search("고속도로", 3)["documents"].meta)
