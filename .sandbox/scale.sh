#!/bin/bash

. "${BASH_SOURCE[0]%/*}/functions.sh"

set -e

DEPLOYMENTS=()

for name in $(kubectl -n "$K8S_NS" get deploy -o jsonpath='{.items[*].metadata.name}') ; do
    DEPLOYMENTS+=("deployment/$name")
done

[[ ${#DEPLOYMENTS} > 0 ]] || exit 0

kubectl -n "$K8S_NS" scale --replicas=$1 "${DEPLOYMENTS[@]}" >&2

cat <<EOF
{
    "namespace": "$K8S_NS",
    "replicas": $1
}
EOF