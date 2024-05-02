import os
import subprocess

# Set the base directory where dote.py will be executed
base_dir = "/Users/yejin/TEBench/DOTE/networking_envs/data/Abilene"
dote_script_path = "../../../dote.py"  # Relative path to the dote.py script

# Define the types of noise and their levels to iterate over
noise_types = ["Gaussian_Multiplicative_Noise", "Multiplicative_Noise"]  # Add additional noise types here
noise_levels = ["0.2", "0.4", "0.6", "0.8", "1.0", "1.2"]  # Example noise levels

# Specify the ecmp_topo configuration
ecmp_topo = "Abilene"

# Create a directory to store the output files if it doesn't already exist
output_dir = "/Users/yejin/TEBench/Benchmark/results"
os.makedirs(output_dir, exist_ok=True)

# Iterate over each noise type and level
for noise_type in noise_types:
    for level in noise_levels:
        # Construct the path to the traffic matrix directory
        traffic_matrix_dir = f"/Users/yejin/TEBench/traffic-matrices/perturbated/{ecmp_topo}/{noise_type}/{level}/test.opt"

        # Construct the command to execute the dote.py script
        cmd = f"python {dote_script_path} --ecmp_topo {ecmp_topo} --paths_from sp --so_mode test --opt_function MAXUTIL --test_data_path /Users/yejin/TEBench/traffic-matrices/original/Abilene/test --trained_model_path /Users/yejin/TEBench/DOTE/trained_models/Abilene/Abilene_MAXUTIL_epoch_5.pkl"
        opt_function = "MAXUTIL"
        epoch = 5

        # File to store the output
        output_file_path = f"{output_dir}/DOTE/{opt_function}_epoch_{epoch}_{noise_type}_{level}_output.txt"

        # Change working directory, execute the command, and redirect output to a file
        os.chdir(base_dir)
        with open(output_file_path, 'w') as output_file:
            subprocess.run(cmd, shell=True, stdout=output_file, stderr=subprocess.STDOUT)

        # Print completion message for each noise level
        print(f"Completed: {noise_type} with level {level}, results saved to {output_file_path}")
