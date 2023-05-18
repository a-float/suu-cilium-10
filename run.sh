#!/bin/bash

set -x

# start minikube
minikube start --network-plugin=cni --cni=false

# install cilium
cilium install

# enable Hubble
cilium hubble enable
cilium hubble port-forward&

# use minikube's docker to be able to load local images
eval $(minikube docker-env)

# build and load service image
docker build -t simple-service:latest ./simple-service/

# deploy service
kubectl apply -f simple-service/deployment.yaml

