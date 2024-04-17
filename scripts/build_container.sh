#!/bin/bash

workdir=/home/notebook-user
docker run -dt --name myunstructured  \
    --network my-network \
    -v ${PWD}/src/unstructured:${workdir}/src \
    -v ${PWD}/output:${workdir}/output \
    -v ${PWD}/input:${workdir}/input \
    unstructured:latest