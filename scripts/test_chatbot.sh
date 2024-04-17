#!/bin/bash
# Note: running container name from llama.cpp image is needed
# `"..."` is needed to break the long string
llamacpp_container_name=llamacpp_server
docker exec -it myunstructured bash -c \
    "python3 src/chatbot.py -u http://${llamacpp_container_name}:8080/completion "`
    `"-i input/pdfs/1207.7214.pdf -q \"What is the mass of the Higgs Boson? "`
    `"Why is this discovery important?\"" 
