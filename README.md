# Pokemon

## Overview
This repository contains the code for the Pokemon application, a simple web service that fetches Pokemon details using the PokeAPI.
It is designed to be deployed on a Kubernetes cluster and includes monitoring with Prometheus and Grafana.

## Prerequisites
- Kubernetes cluster
- Helm
- kubectl
- Docker 

## Installation

1. Clone the repository: `git clone https://github.com/omeritzhaki320/pokemon.git`
    - `cd pokemon`
2. Install the application using the following commands:
    - `kubectl apply -f k8s/deployment.yaml`
    - `kubectl apply -f k8s/service.yaml`
    - `kubectl apply -f k8s/hpa.yaml`
   
3. Install the monitoring using the following commands:
   - `helm install prometheus ./charts/prometheus --namespace monitoring --create-namespace -f ./charts/prometheus/values.yaml`
   - `helm install grafana ./charts/grafana --namespace monitoring --create-namespace -f ./charts/grafana/values.yaml`

## Usage
1. Access to Pokemon: `kubectl port-forward svc/server-service 8000:80 -n pokemon`
 - URL: http://localhost:8000/pokemon
2. Access Grafana: `kubectl port-forward svc/grafana 3000:80 -n monitoring`
 - URL: http://localhost:3000
3. Access Prometheus: `kubectl port-forward svc/prometheus-server 9090:80 -n monitoring`
 - URL: http://localhost:9090

## CI/CD Pipeline
A GitHub Actions CI/CD pipeline is set up to automate the deployment process. On each push to the master branch, the pipeline will:
1. Build the Docker image
2. Push the image to Docker Hub
3. Update the Kubernetes deployment with the new image

Ensure the following secrets are set in your GitHub repository:

 - DOCKER_USERNAME: Your Docker Hub username
 - DOCKER_PASSWORD: Your Docker Hub password
 - KUBECONFIG: Base64 encoded kubeconfig for your Minikube cluster

The workflow file is located at .github/workflows/deploy.yml.

## Cleanup
- `helm uninstall prometheus`
- `helm uninstall grafana`
- `kubectl delete namespace monitoring`
- `kubectl delete namespace pokemon`
