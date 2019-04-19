from mcr.microsoft.com/mssql/server:2017-latest

ENV ACCEPT_EULA=Y
ENV SA_PASSWORD=Password1

RUN apt-get update && apt-get install -y python3 python3-pip unixodbc-dev

ADD requirements.txt /source_tests/
RUN pip3 install -r /source_tests/requirements.txt

ADD . /source_tests
WORKDIR /source_tests

CMD python3 sql_server.py
