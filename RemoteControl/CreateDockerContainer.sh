#!/bin/bash
#create docker image
docker build -t remotecontrol .
#create docker container and run
docker run -d   -p 5001:5001   --add-host=host.docker.internal:host-gateway   --name remotecontrol   remotecontrol
#stop docker container
docker stop remotecontrol

#run docker container
docker start remotecontrol