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

Here's the example with GCP identity federation:

```sh
# Provide the following environments
export PROJECT_NUMBER=...
export IDFED_POOL_ID=...
export IDFED_PROVIDER_ID=...
export SERVICE_ACCOUNT_EMAIL=...
cat <<EOF | cs secret create --shared shared/gcp-account.json
{
    "type": "external_account",
    "audience": "//iam.googleapis.com/projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/${IDFED_POOL_ID}/providers/${IDFED_PROVIDER_ID}",
    "subject_token_type": "urn:ietf:params:oauth:token-type:jwt",
    "token_url": "https://sts.googleapis.com/v1/token",
    "service_account_impersonation_url": "https://iamcredentials.googleapis.com/v1/projects/-/serviceAccounts/${SERVICE_ACCOUNT_EMAIL}:generateAccessToken",
    "credential_source": {
        "file": "/run/sandbox/fs/metadata/1000/token",
        "format": {
            "type": "text"
        }
    }
}
EOF
export GKE_MASTER_CERT_B64=...base64 encoded GKE master certificate
export GKE_MASTER_IP=...
cat <<EOF | cs secret create --shared shared/kubeconfig-demo.yaml
apiVersion: v1
kind: Config
contexts:
- name: demo
  context:
    cluster: demo
    namespace: default
    user: demo-user
clusters:
- name: demo
  cluster:
    certificate-authority-data: ${GKE_MASTER_CERT_B64}
    server: https://${GKE_MASTER_IP}
users:
- name: demo-user
  user:
    exec:
      apiVersion: client.authentication.k8s.io/v1beta1
      command: idfed
      args:
      - gke
current_context: demo
EOF
```

### Snapshots

Using the `.sandbox/snapshot/base.sh` to install software in an empty workspace and create a
base snapshot from there:

```sh
sudo .sandbox/snapshot/base.sh
cs snapshot create shared/base-boutique-r1
```

### App

Create an App using `.sandbox/app.yaml`:

```sh
cs app create shared/boutique .sandbox/app.yaml
```
