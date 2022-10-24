#!/bin/bash

. "${BASH_SOURCE[0]%/*}/functions.sh"

kubectl delete ns "$K8S_NS" >&2
