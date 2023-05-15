#!bin/bash

set -x

docker build -t simple-service:latest ./simple-service/

minikube image load simple-service

kubectl create deployment simple-service --image=simple-service

minikube image rm simple-service
