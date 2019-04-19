#!/bin/bash
scp -i ~/.ssh/aretonet.pem -r tests/ Dockerfile requirements.txt script/ docker-compose.yml sql_server.py UserSSH@52.178.119.157:/home/UserSSH/aretonet

