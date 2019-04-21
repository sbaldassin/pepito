#!/bin/bash
script/synch_repo.sh
ssh -i ~/.ssh/aretonet.pem  UserSSH@52.178.119.157 "cd aretonet ; script/api_tests.sh"
