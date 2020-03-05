#!/usr/bin/env bash

cd ./src
python3 -m venv .
source ./bin/activate
python3 -m chariot.api.webserver &
cd ../gui
yarn start & 
sleep 5
yarn run electron
