from mcr.microsoft.com/mssql/server:2017-latest

ENV ACCEPT_EULA=Y
ENV SA_PASSWORD=Password1

RUN apt-get update && apt-get install -y python3 python3-pip unixodbc-dev

ADD . /source_tests
WORKDIR /source_tests

RUN pip3 install -r requirements.txt
