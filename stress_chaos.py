from kube_gather import common_labels

def generate_stress_cpu_experiments(app_info, grouped_pods, trigger, spec_config):
    """
    Generates StressChaos experiments for CPU stress per group using external specification.
    StressChaos uses a "mode" field (e.g., "all") and does not support "suspend".
    """
    namespace = app_info["namespace"]
    experiments = []
    # Load CPU spec values from the external spec file.
    cpu_spec = spec_config.get("cpu", {})
    mode = cpu_spec.get("mode", "all")
    default_workers = cpu_spec.get("workers", 2)
    default_load = cpu_spec.get("load", 80)
    default_duration = cpu_spec.get("duration", "30s")
    
    for group_key, pods in grouped_pods.items():
        labels = common_labels(pods)
        if not labels:
            labels = {"app": app_info["app_label"]}
        experiment = {
            "apiVersion": "chaos-mesh.org/v1alpha1",
            "kind": "StressChaos",
            "metadata": {
                "name": f"stress-cpu-{group_key}",
                "namespace": namespace
            },
            "spec": {
                "mode": mode,
                "selector": {"labelSelectors": labels},
                "stressors": {
                    "cpu": {
                        "workers": default_workers,
                        "load": default_load
                    }
                },
                "duration": default_duration
            }
        }
        experiments.append(experiment)
    return experiments

def generate_stress_memory_experiments(app_info, grouped_pods, trigger, spec_config):
    """
    Generates StressChaos experiments for Memory stress per group using external specification.
    """
    namespace = app_info["namespace"]
    experiments = []
    # Load Memory spec values from the external spec file.
    memory_spec = spec_config.get("memory", {})
    mode = memory_spec.get("mode", "all")
    default_size = memory_spec.get("size", "100M")
    default_workers = memory_spec.get("workers", 1)
    default_duration = memory_spec.get("duration", "30s")
    
    for group_key, pods in grouped_pods.items():
        labels = common_labels(pods)
        if not labels:
            labels = {"app": app_info["app_label"]}
        experiment = {
            "apiVersion": "chaos-mesh.org/v1alpha1",
            "kind": "StressChaos",
            "metadata": {
                "name": f"stress-memory-{group_key}",
                "namespace": namespace
            },
            "spec": {
                "mode": mode,
                "selector": {"labelSelectors": labels},
                "stressors": {
                    "memory": {
                        "size": default_size,
                        "workers": default_workers
                    }
                },
                "duration": default_duration
            }
        }
        experiments.append(experiment)
    return experiments

def generate_stress_chaos_experiments_from_config(app_info, grouped_pods, stress_chaos_config, trigger, spec_config):
    """
    Reads the StressChaos configuration and generates experiments for each enabled subtype per group,
    using the external specification in spec_config.
    """
    experiments = []
    stress_subtypes = stress_chaos_config.get("subtypes", [])
    if any(sub.get("name") == "cpu" and sub.get("enabled") for sub in stress_subtypes):
        experiments.extend(generate_stress_cpu_experiments(app_info, grouped_pods, trigger, spec_config))
    if any(sub.get("name") == "memory" and sub.get("enabled") for sub in stress_subtypes):
        experiments.extend(generate_stress_memory_experiments(app_info, grouped_pods, trigger, spec_config))
    return experiments
