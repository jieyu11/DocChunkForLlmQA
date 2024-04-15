#!/bin/bash
# Note: running container name from llama.cpp image is needed
# `"..."` is needed to break the long string
llamacpp_container_name=llamacpp_server
docker exec -it myunstructured bash -c \
    "python3 src/chatbot.py -u http://${llamacpp_container_name}:8080/completion "`
    `"-i input/adobe_pdfs/2256935.pdf -q \"What was the gross "`
    `"profit of three months ended in 2013?\"" 
