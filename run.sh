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
docker build -t job-submitter:latest ./job-submitter/
docker build -t kafka-res-agg:latest ./result-aggregator/
docker build -t add-worker:latest ./calc-workers/add-worker/http/
docker build -t sub-worker:latest ./calc-workers/sub-worker/http/
docker build -t mul-worker:latest ./calc-workers/mul-worker/http/
docker build -t div-worker:latest ./calc-workers/div-worker/http/
docker build -t add-kafka-worker:latest ./calc-workers/add-worker/kafka/
docker build -t sub-kafka-worker:latest ./calc-workers/sub-worker/kafka/
docker build -t mul-kafka-worker:latest ./calc-workers/mul-worker/kafka/
docker build -t div-kafka-worker:latest ./calc-workers/div-worker/kafka/

# deploy service
kubectl apply -f zookeeper.yaml
kubectl apply -f kafka.yaml

kubectl wait --for=condition=ready pod -l app=kafka

kubectl apply -f calc-workers/add-worker/deployment.yaml
kubectl apply -f calc-workers/add-worker/service.yaml

kubectl apply -f calc-workers/sub-worker/deployment.yaml
kubectl apply -f calc-workers/sub-worker/service.yaml

kubectl apply -f calc-workers/mul-worker/deployment.yaml
kubectl apply -f calc-workers/mul-worker/service.yaml

kubectl apply -f calc-workers/div-worker/deployment.yaml
kubectl apply -f calc-workers/div-worker/service.yaml

kubectl apply -f job-submitter/deployment.yaml
kubectl apply -f job-submitter/service.yaml

kubectl apply -f result-aggregator/deployment.yaml
kubectl apply -f result-aggregator/service.yaml

