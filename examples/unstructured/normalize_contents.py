from unstructured_client import UnstructuredClient
from unstructured_client.models import shared
from unstructured_client.models.errors import SDKError

from unstructured.partition.html import partition_html
from unstructured.partition.pptx import partition_pptx
from unstructured.staging.base import dict_to_elements, elements_to_json
import json

# filename = "example_files/medium_blog.html"
filename = "example-docs/example-10k-1p.html"
elements = partition_html(filename=filename)

element_dict = [el.to_dict() for el in elements]
example_output = json.dumps(element_dict[11:15], indent=2)
print(example_output)
print("-----"*10)
print(JSON(example_output))