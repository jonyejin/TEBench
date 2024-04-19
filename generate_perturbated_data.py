import os
from add_perturbation import (
    # add_hybrid_noise,
    add_gaussian_multiplicative_noise,
    add_noise_to_traffic,  # previously known as add_noise_to_traffic
    # apply_noise_with_gradient_descent,
    save_traffic_matrices,
    read_traffic_matrices
)
from collect_optimal import main as collect_optimal_main

def process_and_save_matrices(input_dir, output_base_dir, a_values, file_format):
    """
    Process traffic matrices by applying noise and saving the outputs in structured directories.
    
    :param input_dir: Directory containing the original traffic matrices.
    :param output_base_dir: Base directory to save perturbed traffic matrices.
    :param a_values: List of noise factors to apply, given as a list of floats.
    :param file_format: File format for reading and saving matrices.
    """
    methods = {
        # 'Hybrid Noise': add_hybrid_noise,
        'Gaussian Multiplicative Noise': add_gaussian_multiplicative_noise,
        'Multiplicative Noise': add_noise_to_traffic,
        # 'Gradient Descent Noise': apply_noise_with_gradient_descent
    }

    # Extract the topology name from the input_dir path
    topology_name = os.path.basename(os.path.dirname(input_dir))

    # Iterate over files in input_dir
    for file in os.listdir(input_dir):
        if file.endswith('.hist') and 'toy' not in file:  # Check for .hist extension and absence of 'toy'
            file_path = os.path.join(input_dir, file)
            if os.path.isfile(file_path):  # Make sure it's a file
                traffic_matrices = read_traffic_matrices(file_path)

                for method_name, method_function in methods.items():
                    for a in a_values:
                        perturbed_traffic_matrices = method_function(traffic_matrices, a)
                        # Create the output directory path including the topology name
                        output_dir = os.path.join(output_base_dir, 'perturbated', topology_name, method_name.replace(' ', '_'), str(a))
                        os.makedirs(output_dir, exist_ok=True)
                        # The output file name keeps the same name as the input
                        output_filename = os.path.join(output_dir, 'test.hist')

                        save_traffic_matrices(perturbed_traffic_matrices, output_filename)
                        # Absolute path of the newly created .hist file
                        hist_file_absolute_path = os.path.abspath(output_filename)
                        topology_file_path = os.path.abspath(os.path.join(input_dir, '..', '..', '..', '..', 'data', topology_name, f'{topology_name}_int.txt'))

                        args_for_collect_optimal = [hist_file_absolute_path, 'test', '--topology-file', topology_file_path]
                        collect_optimal_main(args_for_collect_optimal)



# List of folders corresponding to the topologies
test_folders = ["Abilene", "B4", "GEANT", "Kdl", "ASN2k"]

# Assuming 'traffic-matrices' directory is at the same level as 'DOTE' directory
output_base_dir = 'traffic-matrices'

# These values are placeholders, replace with your actual noise levels and file format
noise_levels = [0.2, 0.4, 0.6, 0.8, 1.0, 1.2]
file_format = 'hist'  # File format is .hist

# Iterating over each topology folder
for folder in test_folders:
    input_directory = os.path.join('DOTE/networking_envs/data', folder, 'test')
    process_and_save_matrices(input_directory, output_base_dir, noise_levels, file_format)