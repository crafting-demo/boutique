function fatal() {
    echo "$@" >&2
    exit 1
}

SCRIPT_DIR="$(readlink -nf "${BASH_SOURCE[0]%/*}")"
APP_DIR="$(readlink -nf "$SCRIPT_DIR/..")"
K8S_MANIFEST_FILE="$APP_DIR/services/release/kubernetes-manifests.yaml"
K8S_NS="${APP_NS:-${SANDBOX_APP}-${SANDBOX_ID}}"

[[ -f "$K8S_MANIFEST_FILE" ]] || fatal "Not found: $K8S_MANIFEST_FILE"
