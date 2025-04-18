from kube_gather import common_labels

def generate_pod_kill_experiments(app_info, grouped_pods, kill_percentage, trigger, spec_config):
    """
    Generates PodChaos experiments for the 'pod-kill' subtype using external spec configuration.
    """
    namespace = app_info["namespace"]
    app_label = app_info["app_label"]
    experiments = []
    suspend_state = not trigger
    # Use the pod-kill spec from the configuration file.
    pod_kill_spec = spec_config.get("pod-kill", {})
    default_mode = pod_kill_spec.get("mode", "fixed-percent")
    # Use the provided kill_percentage if not overridden in spec.
    default_value = pod_kill_spec.get("value", str(kill_percentage))
    
    for group_key, pods in grouped_pods.items():
        labels = common_labels(pods)
        if not labels:
            labels = {"app": app_label}
        experiment = {
            "apiVersion": "chaos-mesh.org/v1alpha1",
            "kind": "PodChaos",
            "metadata": {
                "name": f"pod-kill-{group_key}",
                "namespace": namespace
            },
            "spec": {
                "action": "pod-kill",
                "mode": default_mode,
                "value": default_value,
                "selector": {"labelSelectors": labels},
                "suspend": suspend_state
            }
        }
        experiments.append(experiment)
    return experiments

def generate_pod_failure_experiments(app_info, grouped_pods, trigger, spec_config):
    """
    Generates PodChaos experiments for the 'pod-failure' subtype using external spec configuration.
    """
    namespace = app_info["namespace"]
    app_label = app_info["app_label"]
    experiments = []
    suspend_state = not trigger
    pod_failure_spec = spec_config.get("pod-failure", {})
    default_mode = pod_failure_spec.get("mode", "one")
    default_value = pod_failure_spec.get("value", "1")
    
    for group_key, pods in grouped_pods.items():
        labels = common_labels(pods)
        if not labels:
            labels = {"app": app_label}
        experiment = {
            "apiVersion": "chaos-mesh.org/v1alpha1",
            "kind": "PodChaos",
            "metadata": {
                "name": f"pod-failure-{group_key}",
                "namespace": namespace
            },
            "spec": {
                "action": "pod-failure",
                "mode": default_mode,
                "value": default_value,
                "selector": {"labelSelectors": labels},
                "suspend": suspend_state
            }
        }
        experiments.append(experiment)
    return experiments

def generate_container_kill_experiments(app_info, grouped_pods, container_names, trigger, spec_config):
    """
    Generates PodChaos experiments for the 'container-kill' subtype using external spec configuration.
    """
    namespace = app_info["namespace"]
    app_label = app_info["app_label"]
    experiments = []
    suspend_state = not trigger
    container_kill_spec = spec_config.get("container-kill", {})
    default_mode = container_kill_spec.get("mode", "all")
    
    for group_key, pods in grouped_pods.items():
        labels = common_labels(pods)
        if not labels:
            labels = {"app": app_label}
        experiment = {
            "apiVersion": "chaos-mesh.org/v1alpha1",
            "kind": "PodChaos",
            "metadata": {
                "name": f"container-kill-{group_key}",
                "namespace": namespace
            },
            "spec": {
                "action": "container-kill",
                "mode": default_mode,
                "selector": {"labelSelectors": labels},
                "containerNames": container_names,
                "suspend": suspend_state
            }
        }
        experiments.append(experiment)
    return experiments

def generate_pod_chaos_experiments_from_config(app_info, grouped_pods, pod_chaos_config, kill_percentage, trigger, spec_config):
    """
    Reads the PodChaos configuration and generates experiments for each enabled subtype,
    using the external specification in spec_config.
    """
    experiments = []
    pod_subtypes = pod_chaos_config.get("subtypes", [])
    if any(sub.get("name") == "pod-kill" and sub.get("enabled") for sub in pod_subtypes):
        experiments.extend(generate_pod_kill_experiments(app_info, grouped_pods, kill_percentage, trigger, spec_config))
    if any(sub.get("name") == "pod-failure" and sub.get("enabled") for sub in pod_subtypes):
        experiments.extend(generate_pod_failure_experiments(app_info, grouped_pods, trigger, spec_config))
    if any(sub.get("name") == "container-kill" and sub.get("enabled") for sub in pod_subtypes):
        # For container-kill, using a default container name list.
        experiments.extend(generate_container_kill_experiments(app_info, grouped_pods, ["my-container"], trigger, spec_config))
    return experiments
