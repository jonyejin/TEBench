import os
import subprocess

# Configuration
root_dir = os.path.expanduser('/traffic-matrices/perturbated')  # Expand user to get absolute path


# Gather all possible configurations
def gather_configurations(root_dir):
    configurations = []
    for topology in os.listdir(root_dir):
        topology_dir = os.path.join(root_dir, topology)
        if os.path.isdir(topology_dir):
            for noise_type in os.listdir(topology_dir):
                noise_type_dir = os.path.join(topology_dir, noise_type)
                if os.path.isdir(noise_type_dir):
                    for noise_level in os.listdir(noise_type_dir):
                        noise_level_dir = os.path.join(noise_type_dir, noise_level)
                        if os.path.isdir(noise_level_dir):
                            # Count .pkl files to set slice-test-stop
                            pkl_files = [f for f in os.listdir(noise_level_dir) if f.endswith('.pkl')]
                            slice_test_stop = len(pkl_files) - 1
                            configurations.append((topology, noise_type, noise_level, slice_test_stop))
    return configurations


# Execute the script for each configuration and save output to a file
def run_teal_script(configurations):
    for topology, noise_type, noise_level, slice_test_stop in configurations:
        command = (
            f"python teal.py --obj min_max_link_util --topo {topology}.json --epochs 0 "
            f"--perturbation_directory {root_dir} --noise_level {noise_level} "
            f"--noise_type {noise_type} --mode test --slice-train-start 0 --slice-train-stop 0 "
            f"--slice-val-start 0 --slice-val-stop 0 --slice-test-start 1 --slice-test-stop {slice_test_stop}"
        )
        output_file_path = f"{root_dir}/{topology}_{noise_type}_{noise_level}_output_min_max_link_util.txt"
        print("Running command:", command)
        print("Saving output to:", output_file_path)

        # Execute command and save output to a file
        with open(output_file_path, "w") as output_file:
            process = subprocess.run(command, shell=True, stdout=output_file, stderr=subprocess.STDOUT)


# Gather configurations and run the script
configurations = gather_configurations(root_dir)
run_teal_script(configurations)
