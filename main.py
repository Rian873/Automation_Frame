import argparse
import yaml
from kube_gather import gather_app_info, group_pods_by_owner, send_experiments_to_chaos_mesh
from pod_chaos import generate_pod_chaos_experiments_from_config
from network_chaos import generate_network_chaos_experiments_from_config
from stress_chaos import generate_stress_chaos_experiments_from_config

def load_spec(file_path):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)

def main():
    parser = argparse.ArgumentParser(description="Generate Chaos Mesh experiments")
    parser.add_argument("--namespace", default="default", help="Kubernetes namespace")
    parser.add_argument("--app_label", default="my-app", help="App label to filter resources")
    parser.add_argument("--kill_percentage", type=int, default=50, help="Percentage of pods to kill (used for pod-kill)")
    parser.add_argument("--apply", action="store_true", help="Apply experiments to Chaos Mesh")
    parser.add_argument("--trigger", action="store_true", help="Trigger experiments immediately (unsuspend)")
    parser.add_argument("--config", default="config.yaml", help="Path to the main config YAML file")
    parser.add_argument("--pod_spec", default="pod_chaos_spec.yaml", help="Path to the PodChaos specification YAML file")
    parser.add_argument("--network_spec", default="network_chaos_spec.yaml", help="Path to the NetworkChaos specification YAML file")
    parser.add_argument("--stress_spec", default="stress_chaos_spec.yaml", help="Path to the StressChaos specification YAML file")
    args = parser.parse_args()

    # Load the main configuration file.
    with open(args.config, "r") as f:
        config_data = yaml.safe_load(f)

    # Determine effective trigger value (command-line flag takes precedence).
    trigger = args.trigger or config_data.get("trigger", False)

    # Gather application information.
    app_info = gather_app_info(args.namespace, args.app_label)
    grouped_pods = group_pods_by_owner(app_info["pods"])

    # Load external specification files.
    pod_spec = load_spec(args.pod_spec)
    network_spec = load_spec(args.network_spec)
    stress_spec = load_spec(args.stress_spec)

    experiments = []

    # Generate PodChaos experiments if enabled.
    if config_data.get("experiments", {}).get("podChaos", {}).get("enabled", False):
        experiments.extend(generate_pod_chaos_experiments_from_config(
            app_info,
            grouped_pods,
            config_data["experiments"]["podChaos"],
            args.kill_percentage,
            trigger,
            pod_spec
        ))

    # Generate NetworkChaos experiments if enabled.
    if config_data.get("experiments", {}).get("networkChaos", {}).get("enabled", False):
        experiments.extend(generate_network_chaos_experiments_from_config(
            app_info,
            grouped_pods,
            config_data["experiments"]["networkChaos"],
            trigger,
            network_spec
        ))

    # Generate StressChaos experiments if enabled.
    if config_data.get("experiments", {}).get("stressChaos", {}).get("enabled", False):
        experiments.extend(generate_stress_chaos_experiments_from_config(
            app_info,
            grouped_pods,
            config_data["experiments"]["stressChaos"],
            trigger,
            stress_spec
        ))

    # Print generated YAML.
    print("\nGenerated Chaos Mesh Experiments YAML:")
    print(yaml.dump_all(experiments, sort_keys=False))

    # Apply experiments if requested.
    if args.apply:
        send_experiments_to_chaos_mesh(experiments)

if __name__ == "__main__":
    main()
