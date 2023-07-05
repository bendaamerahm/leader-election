from kubernetes import client, config, watch
import os

class K8sClient:
    def __init__(self):
        # Load the kube config
        config.load_incluster_config()
        self.v1 = client.CoreV1Api()

    def get_leader(self):
        try:
            # Get the 'leader-election' ConfigMap from the MY_POD_NAMESPACE namespace
            pod_namespace = os.getenv('MY_POD_NAMESPACE')

            config_map = self.v1.read_namespaced_config_map("leader-election", pod_namespace)
            # Return the 'leader' data from the ConfigMap
            return config_map.data["leader"]
        except client.exceptions.ApiException as e:
            # If the ConfigMap doesn't exist or 'leader' key doesn't exist, return None
            if e.status == 404:
                return None
            else:
                raise

    def set_leader(self):
        # Get the current pod name from the environment variable
        pod_name = os.getenv('MY_POD_NAME')

        # Update the 'leader' value in the 'leader-election' ConfigMap
        pod_namespace = os.getenv('MY_POD_NAMESPACE')
        try:
            # Get the existing ConfigMap
            config_map = self.v1.read_namespaced_config_map("leader-election", pod_namespace)
            # Update the 'leader' key with the current pod name
            config_map.data["leader"] = pod_name
            # Update the ConfigMap
            self.v1.replace_namespaced_config_map("leader-election", pod_namespace, config_map)
            print(f"Updated leader to '{pod_name}' in the ConfigMap.")
        except client.exceptions.ApiException as e:
            print(f"Failed to update leader in ConfigMap: {e}")

    def watch_configmap(self):
        # Create a watch object
        w = watch.Watch()

        # Start watching the 'leader-election' ConfigMap in the 'default' namespace
        pod_namespace = os.getenv('MY_POD_NAMESPACE')
        for event in w.stream(self.v1.list_namespaced_config_map, pod_namespace):
            # If the 'leader-election' ConfigMap is modified
            if event['object'].metadata.name == "leader-election" and event['type'] == 'MODIFIED':
                print("ConfigMap 'leader-election' has been modified")
                # Print the new data
                print(f"New data: {event['object'].data}")
                # Stop watching after a change is detected
                w.stop()

    def restart_pod(self):
        # Get the pod name from the environment variable set in the Deployment
        pod_name = os.getenv("MY_POD_NAME")

        # Delete the current pod
        try:
            pod_namespace = os.getenv('MY_POD_NAMESPACE')
            self.v1.delete_namespaced_pod(pod_name, pod_namespace)
            print(f"Pod {pod_name} deleted successfully. A new one will be recreated automatically.")
        except client.exceptions.ApiException as e:
            print(f"Failed to delete pod {pod_name}: {e}")
