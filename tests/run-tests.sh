#!/bin/bash

JOB_NAME="mbl-cli"
BUILD_NUMBER="0.1.1"

sudo docker build -t build -f ./Dockerfile ../
sudo docker run  --name $JOB_NAME-$BUILD_NUMBER-test build
sudo docker cp $JOB_NAME-$BUILD_NUMBER-test:/mbl-cli/report $PWD
sudo docker rm $JOB_NAME-$BUILD_NUMBER-test

