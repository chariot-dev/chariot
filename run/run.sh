#!/usr/bin/env bash

# Kill child processes on exit
trap 'kill $(jobs -p)' EXIT

bash run-core.sh &

sleep 5
bash run-gui.sh

