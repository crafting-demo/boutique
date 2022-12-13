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

### Prerequisites

- A Kubernetes cluster (either GKE or EKS);
- Config/Credentials in Sandbox secrets for accessing the cluster, and this can be done
  using either of the two options:
  - Setup Identity federation in the target cloud to trust sandbox system as an OIDC
    provider, no actual credentials need to be saved in secrets;
  - Generate credentials from the target cloud and save as secrets.

Please refer to the [doc](https://docs.sandboxes.cloud/docs/access-cloud-provider-from-sandbox) for the details.

### App

Create an App using `.sandbox/app.yaml`:

```sh
cs app create shared/boutique .sandbox/app.yaml
```
