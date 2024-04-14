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
import os

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

    @staticmethod
    def parse_doc(filename):
        elements = None
        if filename.lower().endswith(".pptx"):
            elements = partition_pptx(filename=filename)
        elif filename.lower().endswith(".html"):
            elements = partition_html(filename=filename)
        elif filename.lower().endswith(".pdf"):
            elements = partition_pdf(filename=filename,
                                     strategy="hi_res",
                                     infer_table_structure=True,
                                     hi_res_model_name="yolox")
        else:
            logger.error("File type not supported.")

        return elements
        
    def run(self, filename, outputname=None):
        """
        Partitions the document specified by filename and saves the resulting
            elements as a JSON file with the name outputname.

        Args:
        - filename (str): The name of the document file to be partitioned.
        - outputname (str): The name of the output JSON file. Default is None,
            where the output is not saved to disk. 
        
        Returns:
        - None
        """
        elements = self.parse_doc(filename)
        if elements is None:
            logger.error("Failed to partition document.")
            return None
        element_dict = [el.to_dict() for el in elements]
        if outputname is not None:
            with open(outputname, "w") as outfile:
                json.dump(element_dict, outfile, indent=4)
                logger.info(f"Output saved to {outputname}.")
        return element_dict
    
    def run_dir(self, inputdir, outputdir=None):
        """
        Partitions all the documents in the input directory and saves the resulting elements as JSON files in the output directory.

        Args:
        - inputdir (str): The directory containing the input documents.
        - outputdir (str): The directory where the output JSON files will be saved.

        Returns:
        - None
        """
        logger.info(f"Partitioning all documents in the input directory: {inputdir}")
        doc_idx = 0
        for filename in os.listdir(inputdir):
            basename = os.path.basename(filename).split(".")[0]
            outputname = None
            if outputdir is not None:
                outputname = os.path.join(outputdir, f"{basename}.json")
            self.run(filename=os.path.join(inputdir, filename), outputname=outputname)

            logger.info(f"Partitioned document {doc_idx}: {filename}\n")
            doc_idx += 1

def main():
    t_start = time()
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", type=str, required=True,
                        help="Your input file or folder.")
    parser.add_argument("--output", "-o", type=str, required=True,
                        help="Your output file or folder.")

    args = parser.parse_args()
    dp = DocumentPartition()
    if os.path.isdir(args.input) and os.path.isdir(args.output):
        dp.run_dir(args.input, args.output)
    elif os.path.isfile(args.input) and args.output.lower().endswith(".json"):
        dp.run(args.input, args.output)
    else:
        logger.error("Input and output must be either both directories or both files.")
    tdif = time() - t_start
    logger.info("Time used: %s" % str(timedelta(seconds=tdif)))

if __name__=="__main__": 
    main()