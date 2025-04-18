from kube_gather import common_labels

def generate_network_delay_experiments(app_info, grouped_pods, trigger, spec_config):
    """
    Generates NetworkChaos experiments for the 'delay' subtype per group,
    using external specification from network_chaos_spec.yaml.
    (Note: The 'suspend' field is omitted because your CRD doesn't support it.)
    """
    namespace = app_info["namespace"]
    experiments = []
    # Get the delay specifications from the external spec.
    delay_spec = spec_config.get("delay", {})
    default_latency = delay_spec.get("latency", "100ms")
    default_jitter = delay_spec.get("jitter", "10ms")
    default_correlation = delay_spec.get("correlation", "25")
    
    for group_key, pods in grouped_pods.items():
        labels = common_labels(pods)
        if not labels:
            labels = {"app": app_info["app_label"]}
        experiment = {
            "apiVersion": "chaos-mesh.org/v1alpha1",
            "kind": "NetworkChaos",
            "metadata": {
                "name": f"network-delay-{group_key}",
                "namespace": namespace
            },
            "spec": {
                "action": "delay",
                "mode": "all",
                "delay": {
                    "latency": default_latency,
                    "jitter": default_jitter,
                    "correlation": default_correlation
                },
                "selector": {"labelSelectors": labels}
            }
        }
        experiments.append(experiment)
    return experiments

def generate_network_loss_experiments(app_info, grouped_pods, trigger, spec_config):
    """
    Generates NetworkChaos experiments for the 'loss' subtype per group,
    using external specification.
    """
    namespace = app_info["namespace"]
    experiments = []
    loss_spec = spec_config.get("loss", {})
    default_loss = loss_spec.get("loss", "30")
    default_correlation = loss_spec.get("correlation", "50")
    
    for group_key, pods in grouped_pods.items():
        labels = common_labels(pods)
        if not labels:
            labels = {"app": app_info["app_label"]}
        experiment = {
            "apiVersion": "chaos-mesh.org/v1alpha1",
            "kind": "NetworkChaos",
            "metadata": {
                "name": f"network-loss-{group_key}",
                "namespace": namespace
            },
            "spec": {
                "action": "loss",
                "mode": "all",
                "loss": {
                    "loss": default_loss,
                    "correlation": default_correlation
                },
                "selector": {"labelSelectors": labels}
            }
        }
        experiments.append(experiment)
    return experiments

def generate_network_partition_experiments(app_info, grouped_pods, trigger, spec_config):
    """
    Generates NetworkChaos experiments for the 'partition' subtype per group,
    using external specification.
    """
    namespace = app_info["namespace"]
    experiments = []
    partition_spec = spec_config.get("partition", {})
    default_direction = partition_spec.get("direction", "both")
    
    for group_key, pods in grouped_pods.items():
        labels = common_labels(pods)
        if not labels:
            labels = {"app": app_info["app_label"]}
        experiment = {
            "apiVersion": "chaos-mesh.org/v1alpha1",
            "kind": "NetworkChaos",
            "metadata": {
                "name": f"network-partition-{group_key}",
                "namespace": namespace
            },
            "spec": {
                "action": "partition",
                "mode": "all",
                "partition": {
                    "direction": default_direction
                },
                "selector": {"labelSelectors": labels}
            }
        }
        experiments.append(experiment)
    return experiments

def generate_network_duplicate_experiments(app_info, grouped_pods, trigger, spec_config):
    """
    Generates NetworkChaos experiments for the 'duplicate' subtype per group,
    using external specification.
    """
    namespace = app_info["namespace"]
    experiments = []
    duplicate_spec = spec_config.get("duplicate", {})
    default_duplicate = duplicate_spec.get("duplicate", "40")
    default_correlation = duplicate_spec.get("correlation", "50")
    
    for group_key, pods in grouped_pods.items():
        labels = common_labels(pods)
        if not labels:
            labels = {"app": app_info["app_label"]}
        experiment = {
            "apiVersion": "chaos-mesh.org/v1alpha1",
            "kind": "NetworkChaos",
            "metadata": {
                "name": f"network-duplicate-{group_key}",
                "namespace": namespace
            },
            "spec": {
                "action": "duplicate",
                "mode": "all",
                "duplicate": {
                    "duplicate": default_duplicate,
                    "correlation": default_correlation
                },
                "selector": {"labelSelectors": labels}
            }
        }
        experiments.append(experiment)
    return experiments

def generate_network_corrupt_experiments(app_info, grouped_pods, trigger, spec_config):
    """
    Generates NetworkChaos experiments for the 'corrupt' subtype per group,
    using external specification.
    """
    namespace = app_info["namespace"]
    experiments = []
    corrupt_spec = spec_config.get("corrupt", {})
    default_corrupt = corrupt_spec.get("corrupt", "30")
    default_correlation = corrupt_spec.get("correlation", "50")
    
    for group_key, pods in grouped_pods.items():
        labels = common_labels(pods)
        if not labels:
            labels = {"app": app_info["app_label"]}
        experiment = {
            "apiVersion": "chaos-mesh.org/v1alpha1",
            "kind": "NetworkChaos",
            "metadata": {
                "name": f"network-corrupt-{group_key}",
                "namespace": namespace
            },
            "spec": {
                "action": "corrupt",
                "mode": "all",
                "corrupt": {
                    "corrupt": default_corrupt,
                    "correlation": default_correlation
                },
                "selector": {"labelSelectors": labels}
            }
        }
        experiments.append(experiment)
    return experiments

def generate_network_bandwidth_experiments(app_info, grouped_pods, trigger, spec_config):
    """
    Generates NetworkChaos experiments for the 'bandwidth' subtype per group,
    using external specification (nested under 'tcParameter').
    """
    namespace = app_info["namespace"]
    experiments = []
    bandwidth_spec = spec_config.get("bandwidth", {})
    default_rate = bandwidth_spec.get("rate", "1mbps")
    default_burst = bandwidth_spec.get("burst", 1048576)
    
    for group_key, pods in grouped_pods.items():
        labels = common_labels(pods)
        if not labels:
            labels = {"app": app_info["app_label"]}
        experiment = {
            "apiVersion": "chaos-mesh.org/v1alpha1",
            "kind": "NetworkChaos",
            "metadata": {
                "name": f"network-bandwidth-{group_key}",
                "namespace": namespace
            },
            "spec": {
                "action": "bandwidth",
                "mode": "all",
                "tcParameter": {
                    "bandwidth": {
                        "rate": default_rate,
                        "burst": default_burst
                    }
                },
                "selector": {"labelSelectors": labels}
            }
        }
        experiments.append(experiment)
    return experiments

def generate_network_chaos_experiments_from_config(app_info, grouped_pods, network_chaos_config, trigger, spec_config):
    """
    Reads the NetworkChaos configuration and generates experiments for each enabled subtype per group,
    using external specification from network_chaos_spec.yaml.
    """
    experiments = []
    net_subtypes = network_chaos_config.get("subtypes", [])
    if any(sub.get("name") == "delay" and sub.get("enabled") for sub in net_subtypes):
        experiments.extend(generate_network_delay_experiments(app_info, grouped_pods, trigger, spec_config))
    if any(sub.get("name") == "loss" and sub.get("enabled") for sub in net_subtypes):
        experiments.extend(generate_network_loss_experiments(app_info, grouped_pods, trigger, spec_config))
    if any(sub.get("name") == "partition" and sub.get("enabled") for sub in net_subtypes):
        experiments.extend(generate_network_partition_experiments(app_info, grouped_pods, trigger, spec_config))
    if any(sub.get("name") == "duplicate" and sub.get("enabled") for sub in net_subtypes):
        experiments.extend(generate_network_duplicate_experiments(app_info, grouped_pods, trigger, spec_config))
    if any(sub.get("name") == "corrupt" and sub.get("enabled") for sub in net_subtypes):
        experiments.extend(generate_network_corrupt_experiments(app_info, grouped_pods, trigger, spec_config))
    if any(sub.get("name") == "bandwidth" and sub.get("enabled") for sub in net_subtypes):
        experiments.extend(generate_network_bandwidth_experiments(app_info, grouped_pods, trigger, spec_config))
    return experiments
