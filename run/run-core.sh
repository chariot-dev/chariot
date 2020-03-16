#!/usr/bin/env bash

# Kill child processes on exit
trap 'kill $(jobs -p)' EXIT

cd ../src
python3 -m venv .
source ./bin/activate
python3 -m chariot.api.webserver
