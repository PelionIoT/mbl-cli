#!/bin/bash

JOB_NAME="mbl-cli"
BUILD_NUMBER="0.1.1"

docker build -t build -f ./Dockerfile ../
docker run  --name $JOB_NAME-$BUILD_NUMBER-test build
docker cp $JOB_NAME-$BUILD_NUMBER-test:/mbl-cli/report $PWD
docker rm $JOB_NAME-$BUILD_NUMBER-test

