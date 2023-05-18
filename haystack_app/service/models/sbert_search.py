import os
from haystack.document_stores import ElasticsearchDocumentStore
from haystack.nodes import DensePassageRetriever, TextConverter
from haystack.pipelines import DocumentSearchPipeline
from haystack import Pipeline
from haystack.utils import convert_files_to_docs
import os
from haystack.document_stores import ElasticsearchDocumentStore
from haystack.nodes import TextConverter, PreProcessor, BM25Retriever
from haystack.pipelines import DocumentSearchPipeline, SearchSummarizationPipeline
from haystack import Pipeline

print("now dir ls = ", os.listdir("."))
doc_dir = "./haystack_app/law_data"

# elasticsearch connection and set document store
document_store = ElasticsearchDocumentStore(
    host="elasticsearch_for_haystack_app",
    username="",
    password="",
    index="sbert"
)

# 파일들을 딕셔너리 형태로 변환하여 색인
docs = convert_files_to_docs(doc_dir)
document_store.write_documents(docs)


# Dense Passage Retriever 설정
retriever = DensePassageRetriever(document_store=document_store,
                                 query_embedding_model= "sentence-transformers/paraphrase-multilingual-mpnet-base-v2",
                                 passage_embedding_model= "sentence-transformers/paraphrase-multilingual-mpnet-base-v2",
                                 use_gpu=False)


document_store.update_embeddings(retriever)

# Document Search Pipeline 설정
pipeline = DocumentSearchPipeline(retriever)


#
def search(query, k):
    return pipeline.run(query, params={"Retriever": {"top_k": int(k)}})


if __name__ == "__main__":
    print(search("1", 3)['documents'].meta)
