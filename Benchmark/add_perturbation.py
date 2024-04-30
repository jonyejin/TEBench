import numpy as np
import os
import glob

# General purpose perturbation functions are below

def add_noise_to_traffic(tms, a):
    """
    Methodology: multiplicative noise modeling
    Add noise to traffic matrices by multiplying each element by a factor
    sampled uniformly from the range [1-a, 1+a].

    :param tms: Traffic matrices, a numpy array of shape (num_matrices, num_nodes, num_nodes).
    :param a: Perturbation factor that defines the noise level.
    :return: A numpy array containing perturbed traffic matrices.
    """
    noise_factors = np.random.uniform(1 - a, 1 + a, tms.shape)
    perturbed_tms = tms * noise_factors
    return perturbed_tms

def add_additive_noise(tms, max_noise):
    """
    Methodology: additive noise modeling
    Add additive noise to traffic matrices. Each element is modified by adding a value
    sampled uniformly from [-max_noise, max_noise].

    :param tms: Traffic matrices, a numpy array of shape (num_matrices, num_nodes, num_nodes).
    :param max_noise: Maximum noise level.
    :return: A numpy array containing noise-added traffic matrices.
    """
    noise = np.random.uniform(-max_noise, max_noise, tms.shape)
    noisy_tms = tms + noise
    return noisy_tms

def add_gaussian_multiplicative_noise(tms, sigma):
    """
    Methodology: Gaussian multiplicative noise modeling
    Multiply traffic matrices by Gaussian noise factors. Each element is scaled by a factor
    sampled from a Gaussian distribution centered around 1 with a standard deviation sigma.

    :param tms: Traffic matrices, a numpy array of shape (num_matrices, num_nodes, num_nodes).
    :param sigma: Standard deviation of the Gaussian noise.
    :return: A numpy array containing perturbed traffic matrices.
    """
    noise_factors = np.random.normal(1, sigma, tms.shape)
    noisy_tms = tms * noise_factors
    return noisy_tms

def add_hybrid_noise(tms, a, sigma):
    """
    Methodology: Hybrid noise modeling
    Apply a combination of multiplicative (uniform) and additive (Gaussian) noise to traffic matrices.

    :param tms: Traffic matrices, a numpy array of shape (num_matrices, num_nodes, num_nodes).
    :param a: Factor for uniform multiplicative noise.
    :param sigma: Standard deviation for Gaussian additive noise.
    :return: A numpy array containing perturbed traffic matrices.
    """
    multiplicative_noise = np.random.uniform(1 - a, 1 + a, tms.shape)
    additive_noise = np.random.normal(0, sigma, tms.shape)
    noisy_tms = (tms * multiplicative_noise) + additive_noise
    return noisy_tms


# Functions using the perspective on DOTE's Appendix B are below

def apply_noise_with_gradient_descent(matrix, initial_noise_level, step_size, iterations):
    """
    Methodology: gradient descent
    Apply noise using gradient descent to optimize a hypothetical network performance measure.

    :param matrix: Original traffic matrix.
    :param initial_noise_level: Initial noise level to start optimization.
    :param step_size: Step size for gradient descent.
    :param iterations: Number of iterations for gradient descent.
    :return: Matrix with optimized noise application.
    """
    noise_level = initial_noise_level
    for i in range(iterations):
        # Hypothetical function to calculate the gradient of the performance measure with respect to noise level
        gradient = compute_performance_gradient(matrix, noise_level)
        # Update the noise level based on the gradient
        noise_level -= step_size * gradient
        # Ensure noise level stays within reasonable bounds
        noise_level = max(0, min(noise_level, 1))

    noise = np.random.uniform(-noise_level, noise_level, matrix.shape)
    noisy_matrix = matrix + noise
    return noisy_matrix

def compute_performance_gradient(matrix, noise_level):
    """
    Hypothetical function to compute the gradient of a performance measure with respect to noise level.

    :param matrix: Traffic matrix.
    :param noise_level: Current level of noise applied.
    :return: Gradient of the performance measure.
    """
    # This is a stub function. In practice, this would need to be defined based on the actual performance measure.
    # For demonstration, let's assume a simple performance function that decreases quadratically with noise level.
    return -2 * (1 - noise_level) * np.sum(matrix)


# Matrix utility functions are below

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

# def main(input_dir, output_base_dir, a_values):
#     """
#     Process all .hist files in a directory, add noise, and save the outputs to new directories.

#     :param input_dir: Directory containing .hist files.
#     :param output_base_dir: Base directory to save perturbed traffic matrices.
#     :param a_values: List of noise factors to apply.
#     """
#     # Ensure output base directory exists
#     if not os.path.exists(output_base_dir):
#         os.makedirs(output_base_dir)

#     # List all .hist files in the input directory
#     input_files = glob.glob(os.path.join(input_dir, '*.hist'))

#     for file_path in input_files:
#         # Read traffic matrices from the current file
#         traffic_matrices = read_traffic_matrices(file_path)

#         for a in a_values:
#             # Generate perturbed traffic matrices
#             perturbed_traffic_matrices = add_noise_to_traffic(traffic_matrices, a)

#             # Prepare output directory and filename
#             output_dir = os.path.join(output_base_dir, f'test_noise_{a}')
#             if not os.path.exists(output_dir):
#                 os.makedirs(output_dir)
#             output_filename = os.path.join(output_dir, os.path.basename(file_path))

#             # Save perturbed traffic matrices
#             save_traffic_matrices(perturbed_traffic_matrices, output_filename)
#             print(f"Perturbed traffic matrices for a={a} saved in {output_filename}")


# # Example usage
# if __name__ == "__main__":
#     input_directory = 'DOTE/networking_envs/data/Abilene/test'
#     output_base_directory = 'DOTE/networking_envs/data/Abilene/test_perturb'
#     noise_levels = [0.1, 0.25, 0.35]
#     main(input_directory, output_base_directory, noise_levels)
