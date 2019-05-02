#!/bin/bash
#syncronize repo before to deploy server
echo "Copying files to the server"
./script/synch_repo.sh


# Running deploy server from remote host
echo "Deploying server"
ssh -i ~/.ssh/aretonet.pem -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null UserSSH@52.178.119.157 cd aretonet && ./script/deploy_server.sh
