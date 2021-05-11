#!/usr/bin/env bash

#Check that arguments have been passed in
: "${1:?'Requires environment name argument! Exiting..'}"

ENV_NAME=$1

source  ${ENV_NAME}/bin/activate

python app.py
