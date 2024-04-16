# Document Parsing and Prompting for LLM Question Answering

The following system is designed to parse the given document and use them in the LLM 
question answering phase. The parsed document is first converted into chunks of texts.
The texts are then vectorized, while the embedding vectors are stored in the FAISS database.
The vectorized 
The summarized flow document chunking, prompting and LLM QA are presented in the following flow chart:

![Flow Diagram](images/flow_chart.png)


## Set Up

```bash
python3 -m venv .venv 
source .venv/bin/activate 
```

## Build Private Network with Docker
A private network is needed with more than one docker containers are running and
one container needs to call the others through API requests. The following
command is used to create a network called `my-network`.
```bash
docker network create my-network
docker network ls
```

## Chunking with Unstructured

Following steps are used to run chunking with `unstructured`, which can be found in
the [unstructured github page](https://github.com/Unstructured-IO/unstructured).

### Step 1: Building A Docker Image for Unstructured

Build a docker image with unstructured base image. Add necessary personal tools needed 
for other functions needed. Do it for the only the first time:

```bash
docker pull downloads.unstructured.io/unstructured-io/unstructured:latest
cd docker
source build_docker.sh
```

After that, there should be `unstructured` in the repository list by running `docker images`.

### Step 2: Build A Docker Container with Unstructured Image

* Build a container by running the following script:

```bash
source scripts/build_container.sh
```

which has the following scripts:
```bash
workdir=/home/notebook-user
docker run -dt --name myunstructured  \
    --network my-network \
    -v ${PWD}/src/unstructured:${workdir}/src \
    -v ${PWD}/output:${workdir}/output \
    -v ${PWD}/input:${workdir}/input \
    unstructured:latest
```
As it is shwn above, the `src/unstructured` is mounted to `src/.` in the docker
conainer's working directory.

Now doing `docker ps` should output a container named: `myunstructured`.

### Step 3: Document Partioning

* Execute docker for document partition:
```bash
docker exec -it myunstructured bash -c "python3 src/document_partition.py -i [INPUT] -o [OUTPUT]"
```

Here, both `[INPUT]` and `[OUTPUT]` are either all directories or all files. In the case
that they are directories, all the files in the input directory are looped and executed one
by one. The basename of the file is used as the output file name.

* Execute docker for document chunking:
```bash
docker exec -it myunstructured bash -c "python3 src/chunking.py -i [INPUT] -o [OUTPUT]"
```

where, `[INPUT]` and `[OUTPUT]` are filenames.

### Step 4: Search Capability through FAISS
The chunked text are converted to embedding vectors with `SentenceTransformer` model of
`all-MiniLM-L6-v2`. The vectors are indexed and stored in the FAISS vector database through
`Langchain`.

The command to execute the docker container for document search:

```bash
docker exec -it myunstructured bash -c "python3 src/vector_store.py -i [INPUT] -q \"HERE IS THE QUESTION\""
```

where, `[INPUT]` is the file name. It is then followed by the question using tag `-q`. The results
are the list of text trunks, which are most relevant to the question.


## RAG with Pretrained LLM

### Step 1: Build a Docker Container with LLAMA.CPP

Following the [llama.cpp github page](https://github.com/ggerganov/llama.cpp), 
The docker image `ghcr.io/ggerganov/llama.cpp:server` is used to build the 
docker container to searve the LLM models.

Here is the script for it.
```bash
models_folder=${FOLDER_OF_LLM_MODEL}
model_file=${LLM_MODEL_FILE}

container_name=llamacpp_server
docker run -dt \
    --name ${container_name} \
    -p 8080:8080 -v ${models_folder}:/models \
    --network my-network \
    ghcr.io/ggerganov/llama.cpp:server -m /models/${model_file} \
    -c 512 --host 0.0.0.0 --port 8080
```

For the `model_file`, I have tested with the models from: 
[TheBloke](https://huggingface.co/TheBloke/LLaMa-7B-GGML),
for example, `llama-2-7b-chat.Q2_K.gguf`.

### Step 2: Question Answer with RAG
With `unstructed` for document chunking and vector searching, one can provide 
a document and question 

```bash
llamacpp_container_name=llamacpp_server
docker exec -it myunstructured bash -c \
    "python3 src/chatbot.py -u http://${llamacpp_container_name}:8080/completion "`
    `"-i input/pdfs/1207.7214.pdf -q \"What is the mass of the Higgs Boson? "`
    `"Why is this discovery important?\"" 
```

Where, `1207.7214.pdf` is the paper `Observation of a New Particle in the Search for the Standard`
` Model Higgs Boson with the ATLAS Detector at the LHC` downloaded from `arxiv`. The questions
are `What is the mass of the Higgs Boson? Why is this discovery important?`.

The top 3 chunks that are found to be `closest` to the questions are:

```
Higgs boson, more data are needed to assess its nature in detail.

The Standard Model (SM) of particle physics [1–4] has been tested by many experiments over the last four decades and has been shown to successfully describe high energy particle interactions. However, the mecha- nism that breaks electroweak symmetry in the SM has not been veriﬁed experimentally. This mechanism [5– 10], which gives mass to massive elementary particles, implies the existence of a scalar particle, the SM Higgs boson. The search for the Higgs boson, the only ele- mentary particle in

evidence the discovery of a new particle with mass for 126.0 signal ± strength parameter µ has the value 1.4 0.3 at the ﬁtted mass, which is consistent with the SM Higgs boson hypothesis µ = 1. The decays to pairs of vector bosons whose net electric charge is zero identify the new particle as a neutral boson. The observation in the diphoton channel disfavours the spin-1 hypothe- sis [140, 141]. Although these results are compatible with the hypothesis that the new particle is the Standard Model
```


The prompt is in the following:
```
You are a helpful assistant. You are given the following context:

{matched_chunks}

You are asked to answer the following question:
{questions}

Your answer should be verbose and accurate.
```

The output is found below:
```
The Higgs Boson has a mass of approximately 125 GeV. The discovery of the Higgs Boson is important because it confirms the existence of the Higgs Field, a fundamental concept in the Standard Model of particle physics, which explains how particles acquire mass. The Standard Model of particle physics has been tested by many experiments over the last four decades and has been shown to successfully describe high energy particle interactions. However, the mechanism that breaks electroweak symmetry in the SM, which gives mass to massive elementary particles, has not been veriﬁed experimentally. The discovery of the Higgs Boson, the only ele- mentary particle inevidence the discovery of a new particle with mass for 126.0 signal ± strength parameter µ has the value 1.4 0.3 at the ﬁtted mass, which is consistent with the SM Higgs Boson. This discovery confirms the existence of the Higgs Field, a fundamental concept in the Standard Model of particle physics, which explains how particles acquire mass. This discovery has important implications for our understanding of the fundamental laws of physics and the nature of the universe.
```