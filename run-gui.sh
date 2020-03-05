#!/usr/bin/env bash

cd ./src
python3 -m venv .
source ./bin/activate
cd ../gui
yarn start && yarn run electron
