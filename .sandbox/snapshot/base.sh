#!/bin/bash

function fatal() {
    echo "$@" >&2
    exit 1
}

[[ "$(id -u)" == "0" ]] || fatal "Must run as root!"

# Install dotnet on Ubuntu 20.04
wget https://packages.microsoft.com/config/ubuntu/20.04/packages-microsoft-prod.deb -O /tmp/packages-microsoft-prod.deb
dpkg -i /tmp/packages-microsoft-prod.deb
rm /tmp/packages-microsoft-prod.deb

apt-get update
apt-get install -y iputils-ping iputils-tracepath redis-tools mysql-client postgresql-client dotnet-sdk-6.0
curl -sSLf https://dl.k8s.io/v1.23.13/kubernetes-client-linux-amd64.tar.gz | tar -C /usr/local/bin -zx --strip-components=3
curl -sSLf -o /tmp/awscli.zip https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip
unzip -d /tmp -o /tmp/awscli.zip
/tmp/aws/install
curl -sSLf https://github.com/bronze1man/yaml2json/releases/download/v1.3/yaml2json_linux_amd64 >/usr/local/bin/yaml2json
chmod a+rx /usr/local/bin/yaml2json
curl -sSLf https://github.com/bronze1man/json2yaml/releases/download/1.0/json2yaml_linux_amd64 >/usr/local/bin/json2yaml
chmod a+rx /usr/local/bin/json2yaml
