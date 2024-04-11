from unstructured_client import UnstructuredClient
from unstructured_client.models import shared
from unstructured_client.models.errors import SDKError

from unstructured.partition.html import partition_html
from unstructured.partition.pptx import partition_pptx
from unstructured.partition.pdf import partition_pdf
from unstructured.staging.base import dict_to_elements, elements_to_json
import json
import logging
import argparse
from time import time
from datetime import timedelta

logging.basicConfig(format="%(asctime)s %(levelname)s: %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)


class DocumentPartition:
    """
    A class for partitioning different types of documents (pptx, html, pdf) into smaller elements and saving the output as a JSON file.

    Methods:
    - __init__(): Initializes the DocumentPartition class.
    - run(filename, outputname): Partitions the document specified by filename and saves the resulting elements as a JSON file with the name outputname.
    """

    def __init__(self):
        pass

    def run(self, filename, outputname):
        """
        Partitions the document specified by filename and saves the resulting elements as a JSON file with the name outputname.

        Args:
        - filename (str): The name of the document file to be partitioned.
        - outputname (str): The name of the output JSON file.

        Returns:
        - None
        """
        if filename.lower().endswith(".pptx"):
            elements = partition_pptx(filename=filename)
        elif filename.lower().endswith(".html"):
            elements = partition_html(filename=filename)
        elif filename.lower().endswith(".pdf"):
            elements = partition_pdf(filename=filename)
        else:
            logger.error("File type not supported.")
            return
        element_dict = [el.to_dict() for el in elements]
        with open(outputname, "w") as outfile:
            json.dump(element_dict, outfile, indent=4)
            logger.info(f"Output saved to {outputname}.")

def main():
    t_start = time()
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", type=str, required=True,
                        help="Your input file.")
    parser.add_argument("--output", "-o", type=str, required=True,
                        help="Your output file.")

    args = parser.parse_args()
    dp = DocumentPartition()
    dp.run(args.input, args.output)
    tdif = time() - t_start
    logger.info("Time used: %s" % str(timedelta(seconds=tdif)))

if __name__=="__main__": 
    main()