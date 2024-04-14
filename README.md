# Documents Chunking

## Set Up

```bash
python3 -m venv .venv 
source .venv/bin/activate 
```


## Chunking Algorithms

### Unstructured

#### Docker Run
Following the following commands.

##### Step 1: Building A Docker Image

* Do it for the first time to pull the latest docker image:
```bash
docker pull downloads.unstructured.io/unstructured-io/unstructured:latest
```
* Build own docker image:
```bash
cd docker
source build_docker.sh
```

After that, there should be `unstructured` in the repository list by running `docker images`.

##### Step 2: Build A Docker Container

* Build a container by running the following script:

```bash
source scripts/build_container.sh
```

Now doing `docker ps` should output a container named: `myunstructured`.

##### Step 3: Document Partioning

* Execute docker for document partition:
```
docker exec -it myunstructured bash -c "python3 src/document_partition.py -i [INPUT] -o [OUTPUT]"
```

Here, both `[INPUT]` and `[OUTPUT]` are either all directories or all files. In the case
that they are directories, all the files in the input directory are looped and executed one
by one. The basename of the file is used as the output file name.

* Execute docker for document chunking:
```
docker exec -it myunstructured bash -c "python3 src/chunking.py -i [INPUT] -o [OUTPUT]"
```

where, `[INPUT]` and `[OUTPUT]` are filenames.

* Execute docker for document search:
