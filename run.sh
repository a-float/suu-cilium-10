#!/bin/bash

set -x

# start minikube
minikube start --network-plugin=cni --cni=false --nodes 2

# install cilium
# cilium install

# enable Hubble
# cilium hubble enable --ui

# use minikube's docker to be able to load local images
eval $(minikube docker-env)

# build and load service image
docker build -t job-submitter:latest ./job-submitter/
docker build -t kafka-res-agg:latest ./result-aggregator/
docker build -t http-worker:latest ./workers/http/
docker build -t kafka-worker:latest ./workers/kafka/

# deploy service
kubectl apply -f zookeeper.yaml
kubectl apply -f kafka.yaml

kubectl wait --for=condition=ready pod -l app=zookeeper
kubectl wait --for=condition=ready pod -l app=kafka

kubectl apply -f ./workers/deployment-add.yaml
kubectl apply -f ./workers/deployment-sub.yaml
kubectl apply -f ./workers/deployment-mul.yaml
kubectl apply -f ./workers/deployment-div.yaml
kubectl apply -f ./workers/services.yaml

kubectl apply -f job-submitter/deployment.yaml
kubectl apply -f job-submitter/service.yaml

kubectl apply -f result-aggregator/deployment.yaml
kubectl apply -f result-aggregator/service.yaml

