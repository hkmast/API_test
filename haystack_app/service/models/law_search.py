from haystack.document_stores import ElasticsearchDocumentStore
from haystack.nodes import BM25Retriever, DensePassageRetriever
from haystack.pipelines import DocumentSearchPipeline
from haystack.utils import convert_files_to_docs, fetch_archive_from_http


def con_elastic(host, index):
    return ElasticsearchDocumentStore(
        host=host,
        username="",
        password="",
        index=index,
    )


# elastic search 호스트 이름 정의 / local: "localhost", docker: "elasticsearch_for_haystack_app"
ELASTIC_HOST_NAME = "localhost"

# 판례 sbert
document_store_law_sb = con_elastic(ELASTIC_HOST_NAME, "law_sb")
# 판례 bm25
document_store_law_bm = con_elastic(ELASTIC_HOST_NAME, "law_bm")


# s3에서 데이터 저장
doc_dir = "law_data"
s3_url = "https://d2p6g4vi9p0tds.cloudfront.net/fault_rate/fault_rate.zip"
fetch_archive_from_http(url=s3_url, output_dir=doc_dir)


# 파일들을 딕셔너리 형태로 변환하여 색인
docs = convert_files_to_docs(dir_path=doc_dir, clean_func=None)
print(f"data set len: {len(docs)}")

# 판례 insert sbert
document_store_law_sb.write_documents(docs)
print(f"data insert len (law_sb): {len(document_store_law_sb.get_all_documents())}")
# 판례 insert bm25
document_store_law_bm.write_documents(docs)
print(f"data insert len (law_bm): {len(document_store_law_bm.get_all_documents())}")


# 판례 sbert retriever / Dense Passage Retriever 설정
retriever_law_sb = DensePassageRetriever(
    document_store=document_store_law_sb,
    query_embedding_model="sentence-transformers/paraphrase-multilingual-mpnet-base-v2",  # 다국어에 어울리는 임베딩
    passage_embedding_model="sentence-transformers/paraphrase-multilingual-mpnet-base-v2",  # 다국어에 어울리는 임베딩
    use_gpu=True,
)
# 판례 bm25 retriever / BM25 Retriever 설정
retriever_law_bm = BM25Retriever(document_store=document_store_law_bm)


# 판례 sbert embedding_model에 맞춰서 임베딩
document_store_law_sb.update_embeddings(retriever_law_sb)


# 판례 sbert pipeline / Document Search Pipeline 설정
pipeline_law_sb = DocumentSearchPipeline(retriever_law_sb)
# 판례 bm25 pipeline / Document Search Pipeline 설정
pipeline_law_bm = DocumentSearchPipeline(retriever_law_bm)


# sbert 검색 함수
def search_law_sb(query, k):
    return pipeline_law_sb.run(query, params={"Retriever": {"top_k": int(k)}})


# bm25 검색 함수
def search_law_bm(query, k):
    return pipeline_law_bm.run(query, params={"Retriever": {"top_k": int(k)}})


# hybrid 검색 함수
def search_law_hybrid(query, k):
    return 0


# 테스트
if __name__ == "__main__":
    res = search_law_bm("고속도로", 3)["documents"]
    print(res)
    print([re.meta["name"] for re in res])
