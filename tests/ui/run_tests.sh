#!/bin/bash
docker-compose down 
docker-compose up --build -d
sleep 20
docker-compose run -e BROWSER=chrome test_runner ./run.sh
