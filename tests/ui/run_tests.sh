#!/bin/bash
docker-compose -f tests/ui/docker-compose.yml down 
docker-compose -f tests/ui/docker-compose.yml up --build -d
sleep 20
docker-compose -f tests/ui/docker-compose.yml run -e BROWSER=chrome test_runner ./run.sh
