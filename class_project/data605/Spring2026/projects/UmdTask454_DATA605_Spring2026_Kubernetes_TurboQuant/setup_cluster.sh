#!/bin/bash
# Builds the embedder + ingester images, loads them into minikube,
# and applies the static k8s manifests (namespace, embedder, HPA).
# Run on the host. Idempotent.
set -e

cd "$(dirname "${BASH_SOURCE[0]}")"

mkdir -p data/images data/embeddings

if ! minikube status >/dev/null 2>&1; then
    minikube start
fi
minikube addons enable metrics-server

echo "Building embedder image"
docker build -t tq-embedder services/embedder

echo "Building ingester image"
docker build -t tq-ingester services/ingester

echo "Loading images into minikube"
minikube image load tq-embedder
minikube image load tq-ingester

echo "Applying static manifests"
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/embedder-deployment.yaml
kubectl apply -f k8s/embedder-service.yaml
kubectl apply -f k8s/embedder-hpa.yaml

echo "Waiting for embedder to be ready"
kubectl wait --for=condition=Available --timeout=180s deployment/embedder -n turboquant

echo
echo "Cluster is ready. Leave this terminal running."
