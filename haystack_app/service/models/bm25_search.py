import os
from haystack.pipelines.standard_pipelines import TextIndexingPipeline
from haystack.document_stores import InMemoryDocumentStore
from haystack.nodes import BM25Retriever
from haystack.nodes import FARMReader
from haystack.pipelines import DocumentSearchPipeline


doc_dir = "./law_data"
files_to_index = [doc_dir + "/" + f for f in os.listdir(doc_dir) if f.endswith(".txt")]

# set document store
document_store = InMemoryDocumentStore(use_bm25=True)

# set data(pipeline)
indexing_pipeline = TextIndexingPipeline(document_store)
indexing_pipeline.run_batch(file_paths=files_to_index)

# set retriever
retriever = BM25Retriever(document_store=document_store)

# set query pipeline
pipeline = DocumentSearchPipeline(retriever)

def search(query, k):
    return pipeline.run(query, params={"Retriever": {"top_k": int(k)}})


if __name__ == "__main__":
    print(search("테스트", 1))