#!/bin/bash

echo starting PyStock Server

docker build -t pystock:latest .
docker run -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY -e AWS_SESSION_TOKEN -p 8080:8080 -it pystock:latest