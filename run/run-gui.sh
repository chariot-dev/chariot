# Kill child processes on exit
trap 'kill $(jobs -p)' EXIT

bash ./run-headless.sh # only start core if not already running

export CORE_IP=`docker-machine ip default` # get IP address of core

cd ../gui
yarn start &
sleep 5
yarn run electron
