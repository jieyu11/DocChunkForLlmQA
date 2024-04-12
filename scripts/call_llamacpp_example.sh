#!/bin/bash
#
# assuming scripts/launch_llamacpp_container.sh is running at another terminal
# See: https://github.com/ggerganov/llama.cpp/tree/master/examples/server
#
curl --request POST \
    --url http://localhost:8080/completion \
    --header "Content-Type: application/json" \
    --data '{"prompt": "Building a website can be done in 10 simple steps:","n_predict": 128}'
