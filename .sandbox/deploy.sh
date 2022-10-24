#!/bin/bash

. "${BASH_SOURCE[0]%/*}/functions.sh"

# Ignore the error in case namespace exists.
kubectl create ns "$K8S_NS" >&2 || true

# Remove Load Balancer and loadgenerator.
yaml2json < "$K8S_MANIFEST_FILE" | \
    jq -cMr '.|select(.spec.type != "LoadBalancer" and .metadata.name != "loadgenerator")' | \
    kubectl -n "$K8S_NS" apply -f - >&2

cat <<EOF
{
    "namespace": "$K8S_NS"
}
EOF
