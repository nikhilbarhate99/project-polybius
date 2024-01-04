#!/bin/sh

kubectl apply -f redis/redis-deployment.yaml
kubectl apply -f redis/redis-service.yaml

kubectl apply -f rest/rest-deployment.yaml
kubectl apply -f rest/rest-service.yaml

# kubectl apply -f logs/logs-deployment.yaml

kubectl apply -f llm/llm-deployment.yaml

kubectl apply -f minio/minio-external-service.yaml



kubectl port-forward --address 0.0.0.0 service/redis 6379:6379 &

kubectl port-forward -n minio-ns --address 0.0.0.0 service/minio-proj 9000:9000 &
kubectl port-forward -n minio-ns --address 0.0.0.0 service/minio-proj 9001:9001 &


# port forward for rest for local dev
# kubectl port-forward service/rest-svc 5005:5005


# kubectl apply -f expose-rest.yaml

# kubectl apply -f rest/rest-ingress.yaml
