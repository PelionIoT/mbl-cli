#!/bin/bash

JOB_NAME="mbl-cli"
BUILD_NUMBER="0.1.1"

docker build -t build -f Dockerfile .
docker run  --name $JOB_NAME-$BUILD_NUMBER-build build
docker cp $JOB_NAME-$BUILD_NUMBER-build:/mbl-cli/dist $PWD
docker rm $JOB_NAME-$BUILD_NUMBER-build

