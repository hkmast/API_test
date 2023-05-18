from haystack.document_stores import FAISSDocumentStore
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

document_store = FAISSDocumentStore()

print("now dir ls = ", os.listdir("."))
doc_dir = "./haystack_app/law_data"

docs = convert_files_to_docs(doc_dir)
document_store.write_documents(docs)

# Dense Passage Retriever 설정
retriever = DensePassageRetriever(document_store=document_store,
                                 query_embedding_model= "sentence-transformers/paraphrase-multilingual-mpnet-base-v2",
                                 passage_embedding_model= "sentence-transformers/paraphrase-multilingual-mpnet-base-v2",
                                 use_gpu=True)

document_store.update_embeddings(retriever)

# Document Search Pipeline 설정
pipeline = DocumentSearchPipeline(retriever)


#
def search(query, k):
    return pipeline.run(query, params={"Retriever": {"top_k": int(k)}})


if __name__ == "__main__":
    print(search("수산업협동조합중앙회", 1))
