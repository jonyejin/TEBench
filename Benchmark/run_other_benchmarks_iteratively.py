import os
import subprocess

# Configuration
root_dir = os.path.expanduser('/traffic-matrices/perturbated')  # Adjust root directory based on your system setup
# Adjust root directory
scripts = [
    # "path_form.py",
    "top_form.py",
    # "ncflow.py",
    # "pop.py"
]
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
                            pkl_files = [f for f in os.listdir(noise_level_dir) if f.endswith('.pkl')]
                            slice_test_stop = len(pkl_files) - 1
                            configurations.append((topology, noise_type, noise_level, slice_test_stop))
    return configurations[:1]

# Execute the scripts for each configuration
def run_scripts(configurations):
    for topology, noise_type, noise_level, slice_test_stop in configurations:
        tm_dir_path = os.path.join(root_dir, topology, noise_type, noise_level)  # Construct the traffic matrix directory path
        for script in scripts:
            script_name = script.split('.')[0]
            output_dir = os.path.join(tm_dir_path, script_name)
            os.makedirs(output_dir, exist_ok=True)  # Ensure directory is created

            command = (
                f"python {script} --obj max_concurrent_flow --topos {topology}.json "
                f"--slice-start 0 --slice-stop {slice_test_stop} "
                f"--tm-dir {tm_dir_path} "  # Include the traffic matrix directory
            )

            output_file_path = os.path.join(output_dir, f"{topology}_{noise_type}_{noise_level}_output.txt")
            print("Running command:", command)
            print("Saving output to:", output_file_path)

            # Execute command and save output to a file
            with open(output_file_path, "w") as output_file:
                subprocess.run(command, shell=True, stdout=output_file, stderr=subprocess.STDOUT)

# Gather configurations and run the scripts
configurations = gather_configurations(root_dir)
run_scripts(configurations)
