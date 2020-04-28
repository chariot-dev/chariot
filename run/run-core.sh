if [[ $(docker ps -f ancestor=chariot-core --format "{{.ID}}")  ]]; then
    echo "Core instance already running"
else
    cd ../
    docker run -d -p 5000:5000 chariot-core
fi
