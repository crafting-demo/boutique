# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# The build output is platform-independent jars, so the builder runs on the
# build platform and arm64 images build without emulation.
FROM --platform=$BUILDPLATFORM eclipse-temurin:19@sha256:9b0ae96f84fc58a2db048671f381d110195fb150c83eebb200ae39eb47fe6e62 as builder

WORKDIR /app

COPY ["build.gradle", "gradlew", "./"]
COPY gradle gradle
RUN chmod +x gradlew
RUN ./gradlew downloadRepos

COPY . .
RUN chmod +x gradlew
RUN ./gradlew installDist

# The Alpine JRE and the Cloud Profiler agent are amd64-only, so this uses the
# Ubuntu JRE and runs without the profiler.
FROM eclipse-temurin:19.0.1_10-jre@sha256:a7d3887586126d377932cfd4bdd73ae96f152c14a746fc1c623459f62f8377e5 as without-grpc-health-probe-bin

WORKDIR /app
COPY --from=builder /app .

EXPOSE 9555
ENTRYPOINT ["/app/build/install/hipstershop/bin/AdService"]

FROM without-grpc-health-probe-bin

# renovate: datasource=github-releases depName=grpc-ecosystem/grpc-health-probe
ENV GRPC_HEALTH_PROBE_VERSION=v0.4.15
ARG TARGETARCH
ADD https://github.com/grpc-ecosystem/grpc-health-probe/releases/download/${GRPC_HEALTH_PROBE_VERSION}/grpc_health_probe-linux-${TARGETARCH} /bin/grpc_health_probe
RUN chmod +x /bin/grpc_health_probe
