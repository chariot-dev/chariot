#!/usr/bin/env bash

cd ../src
python3 -m venv .
source ./bin/activate
pip3 install -r requirements.txt
