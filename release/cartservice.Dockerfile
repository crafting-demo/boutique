# Multi-arch (linux/amd64, linux/arm64) build of Boutique's cartservice.
#
# The upstream images are amd64-only, and under emulation on Apple Silicon the
# .NET runtime dies with SIGTRAP (exit 133) as soon as it serves a gRPC request,
# which breaks the shop's home page. The other services build from their own
# Dockerfiles under services/src; this one replaces cartservice's because that
# Alpine build cannot target arm64 (see below).
#
# The SDK stage runs on the build platform and cross-publishes for the target,
# so .NET never runs under emulation during the build either.
#
# glibc rather than musl images: Grpc.Tools 2.51.0 ships a glibc-linked protoc,
# which cannot execute on Alpine and fails the build with a misleading
# "No such file or directory".
#
# Build context: services/src/cartservice/src
#   docker buildx build --platform linux/amd64,linux/arm64 \
#     -f release/cartservice.Dockerfile services/src/cartservice/src

FROM --platform=$BUILDPLATFORM mcr.microsoft.com/dotnet/sdk:7.0 AS builder
ARG TARGETARCH
WORKDIR /app
COPY cartservice.csproj .
RUN RID="linux-$([ "$TARGETARCH" = amd64 ] && echo x64 || echo "$TARGETARCH")" && \
    echo "$RID" >/rid && \
    dotnet restore cartservice.csproj -r "$RID"
COPY . .
RUN dotnet publish cartservice.csproj \
    -p:PublishSingleFile=true \
    -r "$(cat /rid)" \
    --self-contained true \
    -p:PublishTrimmed=True \
    -p:TrimMode=Link \
    -c release \
    -o /cartservice \
    --no-restore

FROM mcr.microsoft.com/dotnet/runtime-deps:7.0
ARG TARGETARCH
WORKDIR /app
COPY --from=builder /cartservice .

# Kept for parity with the upstream image, for gRPC health probes.
ENV GRPC_HEALTH_PROBE_VERSION=v0.4.15
ADD https://github.com/grpc-ecosystem/grpc-health-probe/releases/download/${GRPC_HEALTH_PROBE_VERSION}/grpc_health_probe-linux-${TARGETARCH} /bin/grpc_health_probe
RUN chmod +x /bin/grpc_health_probe

EXPOSE 7070
ENV DOTNET_EnableDiagnostics=0 \
    ASPNETCORE_URLS=http://*:7070
USER 1000
ENTRYPOINT ["/app/cartservice"]
