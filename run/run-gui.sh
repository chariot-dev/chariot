#!/usr/bin/env bash

# Kill child processes on exit
trap 'kill $(jobs -p)' EXIT

cd ../gui
yarn start & 
sleep 5
yarn run electron
