#!/bin/bash
scp -i ~/.ssh/aretonet.pem -r tests/ Dockerfile requirements.txt script/ UserSSH@52.178.119.157:/home/UserSSH/aretonet
