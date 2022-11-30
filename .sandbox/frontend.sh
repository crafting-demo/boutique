#!/bin/bash

while true; do
    # Try to find out load balancer IP (e.g. on GKE).
    HOST=$(kubectl -n $APP_NS get svc frontend-external -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
    # Try to find out the load balancer hostname (e.g. on EKS).
    [[ -n "$HOST" ]] || HOST=$(kubectl -n $APP_NS get svc frontend-external -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
    if [[ -z "$HOST" ]]; then
        echo "External load balancer IP/Hostname unavailable ..."
        sleep 1
        continue
    fi
    echo "External load balancer: $HOST"
    socat TCP-LISTEN:8000,fork,reuseaddr "TCP-CONNECT:$HOST:80"
done
