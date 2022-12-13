FROM golang:1.19 AS gotools
RUN \
    go install -v github.com/uudashr/gopkgs/v2/cmd/gopkgs@latest && \
    go install -v github.com/ramya-rao-a/go-outline@latest && \
    go install -v github.com/cweill/gotests/gotests@latest && \
    go install -v github.com/fatih/gomodifytags@latest && \
    go install -v github.com/josharian/impl@latest && \
    go install -v github.com/haya14busa/goplay/cmd/goplay@latest && \
    go install -v github.com/go-delve/delve/cmd/dlv@latest && \
    go install -v github.com/go-delve/delve/cmd/dlv@master && \
    go install -v honnef.co/go/tools/cmd/staticcheck@latest && \
    go install -v golang.org/x/tools/gopls@latest

FROM ubuntu:22.04
# Base system.
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y tzdata locales locales-all sudo && \
    update-locale LANG=en_US.UTF-8 && \
    sed -i -r 's/^(%sudo\s).+$/\1ALL=(ALL) NOPASSWD:ALL/g' /etc/sudoers && \
    (echo y && echo y) | DEBIAN_FRONTEND=noninteractive unminimize && \
    apt-get install -y \
        bash-builtins \
        bash-completion \
        ca-certificates \
        gpg \
        xz-utils \
        nano \
        vim-nox \
        emacs-nox \
        git \
        curl \
        wget \
        socat \
        telnet \
        netcat \
        man-db \
        zip p7zip \
        tmux \
        screen \
        tree \
        jq \
        cmake \
        make \
        autoconf \
        pkg-config \
        build-essential \
        gdb gdbserver \
        clang \
        clangd \
        llvm \
        virtualenv \
        python3-pip \
        openssh-client \
        openssh-server \
        hexedit \
        iproute2 \
        tcpdump \
        iptables \
        iputils-ping \
        iputils-arping \
        iputils-tracepath \
        rsync \
        strace \
        zsh \
        redis-tools \
        mysql-client \
        postgresql-client && \
        apt-get clean -y
# Additional tools.
RUN curl -sSLf https://dl.k8s.io/v1.23.13/kubernetes-client-linux-amd64.tar.gz | tar -C /usr/local/bin -zx --strip-components=3 && \
    curl -sSLf -o /tmp/awscli.zip https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip && unzip -d /tmp -o /tmp/awscli.zip && /tmp/aws/install && rm -fr /tmp/aws /tmp/awscli.zip && \
    curl -sSLf https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-409.0.0-linux-x86_64.tar.gz | tar -C /usr/local -zx && \
    curl -sSLf https://github.com/bronze1man/yaml2json/releases/download/v1.3/yaml2json_linux_amd64 >/usr/local/bin/yaml2json && chmod a+rx /usr/local/bin/yaml2json && \
    curl -sSLf https://github.com/bronze1man/json2yaml/releases/download/1.0/json2yaml_linux_amd64 >/usr/local/bin/json2yaml && chmod a+rx /usr/local/bin/json2yaml
# Home directory skeleton.
RUN cp -Trf /etc/skel /etc/skel.sandbox && \
    mkdir -p \
        /etc/skel.sandbox/.vscode-server/extensions \
        /etc/skel.sandbox/.vscode-remote/extensions && \
    echo '. /usr/local/google-cloud-sdk/path.bash.inc' >>/etc/skel.sandbox/.bashrc && \
    echo '. /usr/local/google-cloud-sdk/completion.bash.inc' >>/etc/skel.sandbox/.bashrc && \
    echo 'export PATH="$HOME/go/bin:$PATH"' >>/etc/skel.sandbox/.bashrc && \
    echo 'eval "$(direnv hook bash)"' >>/etc/skel.sandbox/.bashrc
COPY --from=gotools /go /etc/skel.sandbox/go
RUN curl -sSLf -o /tmp/golang.go.vsix https://open-vsx.org/api/golang/Go/0.36.0/file/golang.go-0.36.0.vsix && \
    mkdir /tmp/golang.go -p && \
    unzip -d /tmp/golang.go /tmp/golang.go.vsix && \
    mv /tmp/golang.go/extension /etc/skel.sandbox/.vscode-remote/extensions/golang.go-0.36.0-universal && \
    mv /tmp/golang.go/extension.vsixmanifest /etc/skel.sandbox/.vscode-remote/extensions/golang.go-0.36.0-universal/.vsixmanifest && \
    cp -rf /etc/skel.sandbox/.vscode-remote/extensions/golang.go-0.36.0-universal /etc/skel.sandbox/.vscode-server/extensions/golang.go-0.36.0 && \
    rm -fr /tmp/golang.go /tmp/golang.go.vsix
