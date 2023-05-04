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

## Setup

### Connect a Kubernetes Cluster

Follow the instruction on the Web Console to connect a Kubernetes cluster, e.g.

```sh
cs infra connect kubernetes demo
```

### Create a Template

The [sample template](.sandbox/template.yaml) can be used (modify the value of `KUBERNETES_CLUSTER` to
be the name used in the `cs infra connect kubernetes` command above):

```sh
cs template create boutique .sandbox/template.yaml
```

### Create a Sandbox

The created Template can be used to create a sandbox and when the new sandbox launches, a new deployment
will be created in a dedicated namespace (named as `APP_NS` defined in the template).
And it can be directly accessed using the `shop` endpoint.

### Further Improvement

When launching Web IDE (or connect via VSCode), there's no extension installed.
The IDE may prompt for installing the [recommended extensions](.vscode/extensions.json), and after installing
the Golang extension, additional Go tools must also be installed.

To make the sandbox ready for use right after launch, the extensions and additional Go tools can be baked in
a home snapshot. From a running sandbox:

```sh
.sandbox/snapshot/home.sh
cs snapshot create --home home-boutique-v1
```

Then update the template by adding:

```yaml
home_snapshot: home-boutique-v1
```

to the workspace.

Create another sandbox from the updated sandbox, and launch Web IDE. Now everything should be ready.
