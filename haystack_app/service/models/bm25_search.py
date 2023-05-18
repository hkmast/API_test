import os
from haystack.document_stores import ElasticsearchDocumentStore
from haystack.nodes import DensePassageRetriever, TextConverter
from haystack.pipelines import DocumentSearchPipeline
from haystack import Pipeline
from haystack.utils import convert_files_to_docs
import os
from haystack.document_stores import ElasticsearchDocumentStore, InMemoryDocumentStore
from haystack.nodes import TextConverter, PreProcessor, BM25Retriever
from haystack.pipelines import DocumentSearchPipeline, SearchSummarizationPipeline
from haystack import Pipeline

print("now dir ls = ", os.listdir("."))
doc_dir = "./haystack_app/law_data"

# # Elasticsearch connection and set DocumentStore
# host = os.environ.get("ELASTICSEARCH_HOST", "localhost")
# document_store = ElasticsearchDocumentStore(
#     host=host,
#     username="",
#     password="",
#     index="bm25"
# )

document_store = InMemoryDocumentStore(use_bm25=True, bm25_algorithm="BM25Plus")

# Convert files to dictionaries for indexing
docs = convert_files_to_docs(dir_path=doc_dir, clean_func=None)

# Write documents to DocumentStore
document_store.write_documents(docs)

# Set BM25Retriever
retriever = BM25Retriever(document_store=document_store)

# Set DocumentSearchPipeline
pipeline = DocumentSearchPipeline(retriever)
#
def search(query, k):
    return pipeline.run(query, params={"Retriever": {"top_k": int(k)}})

if __name__ == "__main__":
    # print(search("매수신고인", 3)['documents'])
    bm = search("매수신고인", 3)['documents']
    print(bm)
    
    all_list = [i.meta['name'] for i in bm]

    print(all_list)
    