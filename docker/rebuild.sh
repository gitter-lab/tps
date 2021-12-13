#!/bin/bash
imageName=xx:my-image
containerName=my-container

docker build -t $imageName -f Dockerfile  .

echo Delete old container...
docker rm -f $containerName

echo build new container...
docker run -d -p 5000:5000 --name $containerName $imageName