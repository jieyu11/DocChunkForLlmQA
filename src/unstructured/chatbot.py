import requests
import json
import logging
import argparse
from time import time
from datetime import timedelta
import os
from vector_store import VectorStore


logging.basicConfig(format="%(asctime)s %(levelname)s: %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


class Chatbot:
    def __init__(self, api_url, header={"Content-Type":"application/json"}):
        self.api_url = api_url
        logger.info(f"API URL: {api_url}")
        self.header = header
        logger.info(f"Header: {header}")
        self.vs = VectorStore()
        self.retriever_key = "chatbot"

    def build_retriever(self, inputs: list):
        self.vs.build_retriever(inputs, self.retriever_key)
        logger.info(f"Built vectorstore {self.retriever_key} with {len(inputs)} documents")

    def get_prompt(self, query, top_k=3):
        assert self.retriever_key in self.vs.stores, f"Retriever {self.retriever_key} not found."
        results = self.vs.search(query, self.retriever_key, top_k)
        prompt = f"You are a helpful assistant. You are given the following context:\n"
        for doc in results:
            prompt += doc.page_content
        prompt += f"\nYou are asked to answer the following question:\n{query}\n"
        prompt += f"Your answer should be consice and accurate.\n"
        return prompt
        

    def generate(self, query, n_predict=256, top_k=3):
        # data = {"prompt": "Building a website can be done in 10 simple steps:","n_predict": 128}
        prompt = self.get_prompt(query, top_k)
        data = {"prompt": prompt, "n_predict": n_predict}
        logger.info(f"Data with prompt: {data}")
        response = requests.post(self.api_url, data=json.dumps(data), headers=self.header)
        return response.json()

    def talk(self):
        print("I'm a chatbot. I don't have any conversation.")

    def goodbye(self):
        print("Goodbye!")

def main():
    t_start = time()
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", type=str, required=True,
                        help="Your input file.")
    parser.add_argument("--api-url", "-u", type=str, required=True,
                        help="Your api URL.")
    parser.add_argument("--queries", "-q", type=str, required=True,
                        help="Your queries list.", nargs='+')

    args = parser.parse_args()
    cb = Chatbot(args.api_url)
    assert os.path.isfile(args.input), f"Make sure input {args.input} exists."
    cb.build_retriever([args.input])
    for query in args.queries:
        logger.info(f"The query is: {query}")
        results = cb.generate(query)
        logger.info(f"Results for {results}:")
    tdif = time() - t_start
    logger.info("Time used: %s" % str(timedelta(seconds=tdif)))

if __name__=="__main__": 
    main()