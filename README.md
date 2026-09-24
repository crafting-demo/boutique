# Online Boutique

This is a demo using [microservices-demo](https://github.com/GoogleCloudPlatform/microservices-demo)
by Google Cloud Platform to demonstrate:

- Deploy a multi-microservice app in Kubernetes per sandbox;
- The Kubernetes debugging/development capability provided by the sandbox.

## Demonstration

### Deployment per Sandbox

Sandbox is designed to provide a self-contained, isolated development environment.
The _microservices-demo_ is a good example to be deployed in a shared Kubernetes
cluster based on the lifecycle of a sandbox:

- When a new sandbox is created, the whole App is deployed in a dedicated namespace;
- When a sandbox is suspended, the app is scaled to zero;
- When a sandbox is resumed, the app is scaled out;
- When a sandbox is destroy, the app is undeployed by deleting the namespace.

### Kubernetes Development Support

The workspace in a sandbox can seamlessly replace a running workload in a Kubernetes
cluster (without modifying any resources in the cluster), so the developer is able
to develop and debugging the code from the workspace with everything else integrated
with a live deployment in the cluster.

## Images

[release/kubernetes.yaml](release/kubernetes.yaml) runs the upstream v0.6.0 images, except
`cartservice`. Upstream only publishes amd64 images, and the .NET cartservice crashes under
emulation on Apple Silicon, so this repo publishes a multi-arch (amd64 and arm64) build of the
same source to `ghcr.io/crafting-demo/boutique/cartservice` from
[release/cartservice.Dockerfile](release/cartservice.Dockerfile), using the
[cartservice image](.github/workflows/cartservice-image.yaml) workflow.

## Setup

### Connect a Kubernetes Cluster

Follow the instruction on the Web Console to connect a Kubernetes cluster, e.g.

```sh
cs infra connect kubernetes demo
```

### Create a Template

The [sample templates](.sandbox/templates) can be used (modify the value of `KUBERNETES_CLUSTER` to
be the name used in the `cs infra connect kubernetes` command above):

```sh
cs template create boutique-shared-ns .sandbox/templates/shared-ns.yaml
cs template create boutique-sandbox-ns .sandbox/templates/sandbox-ns.yaml
```

### Create a Sandbox

Create a sandbox from a template to start development.

#### Use Shared Deployment

When template `shared-ns.yaml` is used, it's targeting a shared deployment which must exist ahead of time.
Start Kubernetes Interception with the pre-defined _checkout_ plan with conditional interception.

#### Use per-sandbox Namespace

When template `sandbox-ns.yaml` is used, a deployment in the per-sandbox namespace will be applied during sandbox creation
and removed when sandbox is deleted.
All deployments are scaled to zero during sandbox suspension and restored when sandbox is resumed.
Checkout the `resources` definition for how automation is carried out.
