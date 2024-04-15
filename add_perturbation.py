import numpy as np
import os
import glob


def add_noise_to_traffic(tms, a):
    """
    Add noise to traffic matrices by multiplying each element by a factor
    sampled uniformly from the range [1-a, 1+a].

    :param tms: Traffic matrices, a numpy array of shape (num_matrices, num_nodes, num_nodes).
    :param a: Perturbation factor that defines the noise level.
    :return: A numpy array containing perturbed traffic matrices.
    """
    noise_factors = np.random.uniform(1 - a, 1 + a, tms.shape)
    perturbed_tms = tms * noise_factors
    return perturbed_tms

def read_traffic_matrices(filename):
    """
    Read traffic matrices from a text file. Assumes each matrix is separated by two newlines.

    :param filename: Path to the file containing traffic matrices.
    :return: A numpy array of traffic matrices.
    """
    with open(filename, 'r') as file:
        data = file.read().strip()
    matrices = data.split('\n\n')  # Split into separate matrices
    return np.array([np.loadtxt(matrix.splitlines()) for matrix in matrices])

def save_traffic_matrices(tms, filename):
    """
    Save modified traffic matrices to a text file. Each matrix is separated by two newlines.

    :param tms: Numpy array of traffic matrices to be saved.
    :param filename: Path to the output file.
    """
    with open(filename, 'w') as file:
        for matrix in tms:
            np.savetxt(file, matrix, fmt='%f')
            file.write('\n')  # Separate matrices with two newlines

def main(input_dir, output_base_dir, a_values):
    """
    Process all .hist files in a directory, add noise, and save the outputs to new directories.

    :param input_dir: Directory containing .hist files.
    :param output_base_dir: Base directory to save perturbed traffic matrices.
    :param a_values: List of noise factors to apply.
    """
    # Ensure output base directory exists
    if not os.path.exists(output_base_dir):
        os.makedirs(output_base_dir)

    # List all .hist files in the input directory
    input_files = glob.glob(os.path.join(input_dir, '*.hist'))

    for file_path in input_files:
        # Read traffic matrices from the current file
        traffic_matrices = read_traffic_matrices(file_path)

        for a in a_values:
            # Generate perturbed traffic matrices
            perturbed_traffic_matrices = add_noise_to_traffic(traffic_matrices, a)

            # Prepare output directory and filename
            output_dir = os.path.join(output_base_dir, f'test_noise_{a}')
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            output_filename = os.path.join(output_dir, os.path.basename(file_path))

            # Save perturbed traffic matrices
            save_traffic_matrices(perturbed_traffic_matrices, output_filename)
            print(f"Perturbed traffic matrices for a={a} saved in {output_filename}")


# Example usage
if __name__ == "__main__":
    input_directory = 'DOTE/networking_envs/data/Abilene/test'
    output_base_directory = 'DOTE/networking_envs/data/Abilene/test_perturb'
    noise_levels = [0.1, 0.25, 0.35]
    main(input_directory, output_base_directory, noise_levels)
