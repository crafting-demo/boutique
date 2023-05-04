#!/bin/bash

# This script provisions the home directory for snapshots.
# It must NOT run as root.

function fatal() {
    echo "$@" >&2
    exit 1
}

[[ "$(id -u)" != "0" ]] || fatal "Must NOT run as root!"

mkdir -p ~/.snapshot
mkdir -p ~/.vscode-server/extensions
mkdir -p ~/.vscode-remote/extensions
cat <<EOF >~/.snapshot/includes.txt
.snapshot
.vscode-server/extensions
.vscode-remote/extensions
go
EOF

go install -v github.com/uudashr/gopkgs/v2/cmd/gopkgs@latest
go install -v github.com/ramya-rao-a/go-outline@latest
go install -v github.com/cweill/gotests/gotests@latest
go install -v github.com/fatih/gomodifytags@latest
go install -v github.com/josharian/impl@latest
go install -v github.com/haya14busa/goplay/cmd/goplay@latest
go install -v github.com/go-delve/delve/cmd/dlv@latest
go install -v honnef.co/go/tools/cmd/staticcheck@latest
go install -v golang.org/x/tools/gopls@latest

/opt/sandboxd/vscode/bin/code-server-cs --install-extension golang.go
