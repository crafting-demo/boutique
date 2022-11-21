#!/bin/bash

set -e

DEPLOYMENTS=()

for name in $(kubectl -n "$APP_NS" get deploy -o jsonpath='{.items[*].metadata.name}') ; do
    DEPLOYMENTS+=("deployment/$name")
done

[[ ${#DEPLOYMENTS} > 0 ]] || exit 0

kubectl -n "$APP_NS" scale --replicas=$1 "${DEPLOYMENTS[@]}" >&2

cat <<EOF
{
    "namespace": "$APP_NS",
    "replicas": $1
}
EOF
