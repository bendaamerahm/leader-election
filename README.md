# Leader Election with Kubernetes ConfigMap

This project demonstrates a leader election algorithm using a ConfigMap in Kubernetes. The algorithm ensures that only one pod becomes the leader and performs specific tasks while other pods wait for their turn.

## Prerequisites

- Kubernetes cluster
- `kubectl` command-line tool
- Python 3.6 or later

## Setup

*1.* Clone the repository:
   ```bash
   git clone <repository_url>
   ```
*2.* Navigate to the project directory:
```bash
cd leader-election-k8s-configmap
```

*3.* Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Usage
Make sure you have a running Kubernetes cluster and the kubectl command-line tool properly configured to access the cluster.

Deploy the leader election application:

```bash
kubectl apply -f deployment.yaml
```
Monitor the logs of the pod to observe the leader election process:

```bash
kubectl logs -f <pod_name>
```
Replace <pod_name> with the name of the pod running the leader election application.

Modify the ConfigMap named leader-election to trigger a change in leadership:

```bash
kubectl edit configmap leader-election
```
This will open the ConfigMap in your default text editor. Modify the leader field to change the leader. Save and close the file.

Note: Ensure that the ConfigMap leader-election exists in the same namespace as the application.

Observe the logs of the leader election application to see the leader change and pod restarts.

## Cleanup
To clean up the deployed resources, run the following command:

```bash
kubectl delete -f deployment.yaml
```
This will delete the Deployment, and Kubernetes will automatically remove the associated pods.

## Troubleshooting
If the leader election process or pod restarts are not working as expected, you can check the following:

Verify that the MY_POD_NAME and MY_POD_NAMESPACE environment variables are properly set in the pod.
Check the logs of the pod for any error messages or issues.
Ensure that the ConfigMap leader-election exists in the same namespace as the application.
If you encounter any issues or have questions, please feel free to reach out for assistance.

Happy leader election in Kubernetes!
