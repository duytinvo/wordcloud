#!/usr/bin/env bash

#Check that arguments have been passed in
: "${1:?'Requires environment name argument! Exiting..'}"

ENV_NAME=$1

python3.8 -m venv "${ENV_NAME}"
source  ${ENV_NAME}/bin/activate

pip install --upgrade pip
pip install -r requirements.txt