FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python3.8-dev python3-pip
COPY . /chariot/src
WORKDIR /chariot/src
RUN python3.8 -m pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["python3.8"]
CMD ["-m", "chariot.api.webserver"]
