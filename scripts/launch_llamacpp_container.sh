#!/bin/bash
# found: https://github.com/ggerganov/llama.cpp/tree/master/examples/server
# Use: docker network create my-network
#      docker network ls

models_folder=${HOME}/Workarea/Projects/references/models/TheBloke
model_file=llama-2-7b-chat.Q2_K.gguf

docker run -p 8080:8080 -v ${models_folder}:/models \
    --network my-network \
    ghcr.io/ggerganov/llama.cpp:server -m /models/${model_file} \
    -c 512 --host 0.0.0.0 --port 8080

