FROM python:latest
COPY . /chariot/src
WORKDIR /chariot/src
RUN python3 -m pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["python3"]
CMD ["-m", "chariot.api.webserver"]
