import yaml
from collections import defaultdict
from kubernetes import client, config

def gather_app_info(namespace, app_label):
    config.load_kube_config()

    v1 = client.CoreV1Api()
    apps_v1 = client.AppsV1Api()

    # Gather Pods (including labels and owner references for grouping)
    pods = v1.list_namespaced_pod(namespace, label_selector=f"app={app_label}")
    pod_info = []
    for pod in pods.items:
        pod_info.append({
            "name": pod.metadata.name,
            "ip": pod.status.pod_ip,
            "labels": pod.metadata.labels or {},
            "owner_references": [
                {"kind": ref.kind, "name": ref.name} for ref in pod.metadata.owner_references
            ] if pod.metadata.owner_references else []
        })

    # Additional resources can be gathered here if needed.
    return {
        "namespace": namespace,
        "pods": pod_info,
        "app_label": app_label,
    }

def group_pods_by_owner(pods):
    """
    Groups pods by their owner reference.
    For pods with an owner, the group key is a combination of the owner kind and name (lowercased).
    For pods without an owner reference, the pod's name (lowercased) is used.
    Returns a dict mapping group key to list of pod info dictionaries.
    """
    grouped = defaultdict(list)
    for pod in pods:
        if pod.get("owner_references"):
            owner = pod["owner_references"][0]
            group_key = f"{owner['kind']}-{owner['name']}".lower()
        else:
            group_key = pod["name"].lower()
        grouped[group_key].append(pod)
    return grouped

def common_labels(pods):
    """
    Computes the intersection of labels for a list of pods.
    Returns a dict containing labels common to all pods.
    """
    if not pods:
        return {}
    common = pods[0]["labels"].copy()
    for pod in pods[1:]:
        keys_to_remove = []
        for k, v in common.items():
            if pod["labels"].get(k) != v:
                keys_to_remove.append(k)
        for k in keys_to_remove:
            common.pop(k, None)
    return common

def send_experiments_to_chaos_mesh(experiments):
    """
    Sends the generated experiments to Chaos Mesh by creating the custom resources.
    """
    custom_api = client.CustomObjectsApi()
    for experiment in experiments:
        try:
            # Determine the CRD plural based on experiment kind.
            if experiment["kind"] == "PodChaos":
                plural = "podchaos"
            elif experiment["kind"] == "NetworkChaos":
                plural = "networkchaos"
            elif experiment["kind"] == "StressChaos":
                plural = "stresschaos"
            else:
                print(f"Unsupported experiment kind: {experiment['kind']}")
                continue

            custom_api.create_namespaced_custom_object(
                group="chaos-mesh.org",
                version="v1alpha1",
                namespace=experiment["metadata"]["namespace"],
                plural=plural,
                body=experiment
            )
            print(f"Experiment {experiment['metadata']['name']} created successfully.")
        except Exception as e:
            print(f"Error creating experiment {experiment['metadata']['name']}: {e}")