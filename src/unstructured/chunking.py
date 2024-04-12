from unstructured.chunking.title import chunk_by_title
from unstructured.staging.base import dict_to_elements
from document_partition import DocumentPartition
from langchain_core.documents import Document
from functools import cache

import json
import logging
import argparse
from time import time
from datetime import timedelta
import os

logging.basicConfig(format="%(asctime)s %(levelname)s: %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


class Chunking:
    def __init__(self) -> None:
        self.dp = DocumentPartition()

    @cache
    def get_elements(self, filename):
        elements = self.dp.parse_doc(filename)
        # elements = dict_to_elements(elements)
        elements = chunk_by_title(elements)
        return elements
    
    def langchain_documents(self, filename):
        elements = self.get_elements(filename)
        documents = []
        for element in elements:
            metadata = element.metadata.to_dict()
            del metadata["languages"]
            metadata["source"] = metadata["filename"]
            documents.append(Document(page_content=element.text, metadata=metadata))
        return documents

    def run(self, filename, outputname=None):
        elements = self.get_elements(filename)
        documents = []
        for element in elements:
            metadata = element.metadata.to_dict()
            del metadata["languages"]
            metadata["source"] = metadata["filename"]
            documents.append(element.text)

        if outputname is not None:
            with open(outputname, "w") as outfile:
                json.dump({"documents": documents}, outfile, indent=4)
                logger.info(f"Output saved to {outputname}.")


def main():
    t_start = time()
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", type=str, required=True,
                        help="Your input file or folder.")
    parser.add_argument("--output", "-o", type=str, required=True,
                        help="Your output file or folder.")

    args = parser.parse_args()
    chk = Chunking()
    assert os.path.isfile(args.input), f"Make sure input {args.input} exists."
    chk.run(args.input, args.output)
    tdif = time() - t_start
    logger.info("Time used: %s" % str(timedelta(seconds=tdif)))

if __name__=="__main__": 
    main()