# Documents Chunking

## Set Up

```bash
python3 -m venv .venv 
source .venv/bin/activate 
```


## Chunking Algorithms

### Unstructured

#### Docker Run
Following the following commands:
* Do it for the first time to pull the latest docker image:
```bash
docker pull downloads.unstructured.io/unstructured-io/unstructured:latest
```
* Do it whenever needed a docker container:
```bash
# root in container: /home/notebook-user
docker run -dt --name unstructured  -v \
     ${PWD}/examples/unstructured:/home/notebook-user/src \
     ${PWD}/output:/home/notebook-user/output \
     ${PWD}/input:/home/notebook-user/input \
     downloads.unstructured.io/unstructured-io/unstructured:latest
```
* Execute docker:
```
docker exec -it unstructured bash
```
followed by:
```bash
python3
```
and then:

```python
from unstructured.partition.pdf import partition_pdf
elements = partition_pdf(filename="example-docs/layout-parser-paper-fast.pdf")

from unstructured.partition.text import partition_text
elements = partition_text(filename="example-docs/fake-text.txt")
```

#### Pip Installation
The local installation of the algorithms
can be found here: [Unstructured](https://github.com/Unstructured-IO/unstructured)