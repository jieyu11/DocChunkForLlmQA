#!/bin/bash
# Note: vigilant_cray is the running container from llama.cpp image
# 
docker exec -it myunstructured bash -c "python3 src/chatbot.py -u http://vigilant_cray:8080/completion -i input/adobe_pdfs/2256935.pdf -q \"What was the gross profit of three months ended in 2013?\"" 
