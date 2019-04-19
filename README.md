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

### Running the tests

To run the tests we just do:
 `script/api_tests.sh`
 
It can be done from localhost if all dependencies are installed or it can be
done within a docker container like this

```
docker build -t test_runner .
docker run -it test_runner script/api_tests.sh
```