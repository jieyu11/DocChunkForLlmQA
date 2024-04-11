#!/bin/bash

workdir=/home/notebook-user
docker run -dt --name myunstructured  \
    -v ${PWD}/src/unstructured:${workdir}/src \
    -v ${PWD}/output:${workdir}/output \
    -v ${PWD}/input:${workdir}/input \
    unstructured:latest
