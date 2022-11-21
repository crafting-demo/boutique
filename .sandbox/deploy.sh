#!/bin/bash

# Ignore the error in case namespace exists.
kubectl create ns "$APP_NS" >&2 || true
kubectl -n "$APP_NS" apply -f release/kubernetes.yaml >&2

cat <<EOF
{
    "namespace": "$APP_NS"
}
EOF
