import os
import time
from k8s_client import K8sClient



def main():
    k8s = K8sClient()
    pod_name = os.getenv('MY_POD_NAME')
    while True:
        leader = k8s.get_leader()
        if leader is None or leader == pod_name:
            # If there is no leader, or if this pod is the leader,
            # Watch for changes in the ConfigMap
            k8s.watch_configmap()
            k8s.restart_pod()
            time.sleep(5)
        else:
            # If this pod is not the leader, try to become the leader
            k8s.set_leader()
            time.sleep(5)

if __name__ == '__main__':
    main()
