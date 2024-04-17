from langchain_openai import OpenAIEmbeddings
from chunking import Chunking
from langchain_core.documents import Document
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_community.vectorstores import Chroma
from langchain_community.vectorstores import FAISS

import json
import logging
import argparse
from time import time
from datetime import timedelta
import os

logging.basicConfig(format="%(asctime)s %(levelname)s: %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


class VectorStore:
    def __init__(self) -> None:
        self.chunking = Chunking()
        # self.embeddings = OpenAIEmbeddings()
        self.embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        # self.retrievers = dict()
        self._stores = dict()
    
    @property
    def stores(self):
        return self._stores
        
    def build_retriever(self, filenames: list[str], retriever_key="default") -> None:
        documents = list()
        for name in filenames:
            documents.extend(self.chunking.langchain_documents(name))
        vectorstore = FAISS.from_documents(documents, self.embeddings)
        logger.info(f"Number of indices in db: {vectorstore.index.ntotal}")

        self._stores[retriever_key] = vectorstore
        logger.info(f"Built vectorstore {retriever_key} with {len(documents)} documents")

    def search(self, query: str, retriever_key, top_k=3) -> list[Document]:
        assert retriever_key in self._stores, f"Retriever {retriever_key} not found."
        retriever = self._stores[retriever_key]
        results = retriever.similarity_search(query, k=top_k)
        return results

    def search_queries(self, queries: list[str], retriever_key) -> list[Document]:
        assert retriever_key in self._stores, f"Retriever {retriever_key} not found."
        retriever = self._stores[retriever_key]
        results = list()
        for query in queries:
            results.append(retriever.similarity_search(query, k=5))
        return results
        
def main():
    t_start = time()
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", type=str, required=True,
                        help="Your input file or folder.")
    parser.add_argument("--key", "-k", type=str, default="default", required=False,
                        help="Your vector store key.")
    parser.add_argument("--queries", "-q", type=str, required=True,
                        help="Your queries list.", nargs='+')

    args = parser.parse_args()
    vs = VectorStore()
    inputs = [args.input] if os.path.isfile(args.input) else list()
    if not inputs:
        assert os.path.isdir(args.input), f"Make sure input {args.input} exists."
        for filename in os.listdir(args.input):
            fullname = os.path.join(args.input, filename)
            inputs.append(fullname)

    vs.build_retriever(inputs, args.key)
    for filename, query in zip(inputs, args.queries):
        results = vs.search(query, args.key)
        logger.info(f"Results for {filename}:")
        for doc in results:
            logger.info(f"  {doc.page_content}")
        logger.info("\n")
    tdif = time() - t_start
    logger.info("Time used: %s" % str(timedelta(seconds=tdif)))

if __name__=="__main__": 
    main()