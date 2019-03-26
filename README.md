## API tests

To run the api tests you need to do 2 steps
1. Build the docker container: `docker build . -t test_runner` 
2. Run the tests inside the container: `docker run -it test_runner script/api_tests.sh`

NOTE: All you need to run the tests in localhost or in a ci pipeline, is docker. Check docker documentation about how to install docker: https://docs.docker.com/install/

