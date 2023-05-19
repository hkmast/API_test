import os
from haystack.document_stores import ElasticsearchDocumentStore
from haystack.nodes import DensePassageRetriever
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
    index="sbert_search",
)

# 파일들을 딕셔너리 형태로 변환하여 색인
docs = convert_files_to_docs(doc_dir)
document_store.write_documents(docs)


# Dense Passage Retriever 설정
retriever = DensePassageRetriever(
    document_store=document_store,
    query_embedding_model="sentence-transformers/paraphrase-multilingual-mpnet-base-v2",  # 다국어에 어울리는 임베딩
    passage_embedding_model="sentence-transformers/paraphrase-multilingual-mpnet-base-v2",  # 다국어에 어울리는 임베딩
    use_gpu=False,
)

# embedding_model에 맞춰서 임베딩
document_store.update_embeddings(retriever)

# Document Search Pipeline 설정
pipeline = DocumentSearchPipeline(retriever)


# 검색 함수
def search(query, k):
    return pipeline.run(query, params={"Retriever": {"top_k": int(k)}})

# 테스트
if __name__ == "__main__":
    print(search("고속도로", 3)["documents"].meta)
