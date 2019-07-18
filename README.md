## API tests


### DB access

Since the DB access is limitted to certain IPs and the tests do access the DB 
to assert on it, a test framework server was created to run in the machine 
which IP was whitelisted

Test server code can be found in the `sql_server.py`

The tests will then follow always the same approach:
1. Use the Areto API to create stuff
2. Use the test framework api (running in the whitelisted ip) to make the 
assertions

#### How to run sql queries easily

In order to run sql queries, you have to:
 1. Ssh into the server:
```bash
Ssh -i aretonet.pem UserSSH@52.178.119.157
```

2. Go to aretonet folder:
```bash
cd aretonet
```

3. Execute bash in container
```bash
docker run -it test_runner bash
```

4. Go to utils folder
```bash
/source_tests/tests/utils
```

5. Execute execute_sql_query script
```bash
python3 execute_sql_query.py "EXEC sp_helpindex 'Q_Net_Dw_Fact_Game';"
```



### Running the tests

To run the tests we just do:
 `script/api_tests.sh`
 
It can be done from localhost if all dependencies are installed or it can be
done within a docker container like this

```
docker build -t test_runner .
docker run -it test_runner script/api_tests.sh
```

### Performance

For performance we use locust, a python library that allow you to simulate 
thoudsands of users hitting the API. The performance tests use the same 
foundation as the functional tests for the API, they are just API tests
scaled up too thouthands of users

To run the performance tests, you have to follow these steps

```markdown
1. Install locust: pip3 install locustio
2. python3 -m locust.main -f tests/performance/signup.py --host test
3. Go to localhost:8089 where locust is listening
4. Set the amount of users that you want to simulate and start testing

```
