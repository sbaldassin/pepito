#!/bin/bash

# Copy sql_server.py and testto the server
#echo "Copyng required files......."
#scp -i ~/.ssh/aretonet.pem -r tests/db script Dockerfile docker-compose.yml sql_server.py UserSSH@52.178.119.157:/home/UserSSH/aretonet

# Connect to the sevrver and run Docker compose down, up and build
echo "Docker-compose DOWN......."
docker-compose down

# Connect to the sevrver and run Docker compose down, up and build
echo "Docker-compose UP......."
docker-compose up

# Connect to the sevrver and run Docker compose down, up and build
echo "Docker-compose BUILD......."
docker-compose build
