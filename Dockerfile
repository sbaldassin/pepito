from ubuntu:16.04

RUN apt-get update && apt-get install -y python3 python3-pip

ADD . /source_tests
WORKDIR /source_tests

RUN pip3 install -r requirements.txt
