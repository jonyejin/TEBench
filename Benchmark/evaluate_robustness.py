import numpy as np
import os

def read_traffic_matrix(filename):
    """
    Read a traffic matrix from a file where each matrix is on a single line,
    with elements separated by spaces. Assumes a square matrix.

    :param filename: Path to the file containing the traffic matrix.
    :param num_nodes: The number of nodes (dimension of the square matrix).
    :return: A numpy array representing the traffic matrix.
    """
    data = []
    with open(filename, 'r') as file:
        for line in file:
            # Convert the line to a float array and reshape to a matrix
            matrix_line = np.array(list(map(float, line.split())), dtype=np.float32)
            size = int(np.sqrt(matrix_line.shape[0]))
            matrix = matrix_line.reshape(size, size)
            data.append(matrix)
    return np.array(data)

def calculate_normalized_change(initial_matrix, new_matrix):
    """
    Calculate the normalized change for each element in the traffic matrix.
    :param initial_matrix: Numpy array of the initial traffic matrix.
    :param new_matrix: Numpy array of the new traffic matrix.
    :return: A numpy array of the normalized changes.
    """
    change = new_matrix - initial_matrix
    with np.errstate(divide='ignore', invalid='ignore'):
        normalized_change = np.where(initial_matrix != 0, change / initial_matrix, 0)
    return np.sum(normalized_change)

def calculate_robustness(MCF_rates, optimal_mcf, weight, normalized_changes):
    """
    Calculate a robustness measure integrating both the efficiency of flow across the network and the stability over time.
    :param MCF_rates: Numpy array of Maximum Concurrent Flow rates for each data set.
    :param optimal_mcf: Float, representing the optimal Maximum Concurrent Flow rate.
    :param weight: Float, weighting factor for the normalized changes.
    :param normalized_changes: Numpy array of normalized changes for each data set.
    :return: Calculated robustness measure.
    """
    if not (len(MCF_rates) == len(normalized_changes)):
        raise ValueError("All input lists must have the same length.")
    efficiency = MCF_rates / optimal_mcf  # Calculate efficiency as a ratio to optimal MCF
    weighted_changes = weight * normalized_changes
    robustness = np.sum(efficiency * weighted_changes) / len(MCF_rates)
    return robustness

def read_optimal_mcf(filename):
    """
    Read the optimal MCF value from a file.
    Assumes the file contains a single floating-point number representing the optimal MCF.
    """
    with open(filename, 'r') as file:
        optimal_mcf = float(file.read().strip())
    return optimal_mcf

def main():
    # Matrix files
    initial_filename = '/DOTE/networking_envs/data/Abilene/test/4.hist'
    new_filename = '/Users/yejin/TEBench/DOTE/networking_envs/data/Abilene/test_noise_0.1/4.hist'
    # MCF hists file
    mcf_filename = '/Users/yejin/TEBench/DOTE/networking_envs/data/Abilene/test_noise_0.1/4.opt'
    # Optimal MCF file
    optimal_mcf_filename = '/Users/yejin/TEBench/DOTE/networking_envs/data/Abilene/test_noise_0.1/4.opt'

    initial_matrices = read_traffic_matrix(initial_filename)
    new_matrices = read_traffic_matrix(new_filename)
    MCF_rates = np.loadtxt(mcf_filename)
    optimal_mcf = read_optimal_mcf(optimal_mcf_filename)  # Read the optimal MCF value

    normalized_changes = calculate_normalized_change(initial_matrices, new_matrices)
    print(normalized_changes)

    weight = 0.2
    robustness_measure = calculate_robustness(MCF_rates, optimal_mcf, weight, normalized_changes)
    print(f"Calculated Robustness Measure: {robustness_measure}")

    # Determine the directory of the MCF file
    directory = os.path.dirname(mcf_filename)
    result_filename = os.path.join(directory, 'robustness_measure.txt')

    # Write results to a file in the same directory as the MCF file
    with open(result_filename, 'w') as file:
        file.write("File Details:\n")
        file.write(f"Initial Traffic Matrix File: {initial_filename}\n")
        file.write(f"New Traffic Matrix File: {new_filename}\n")
        file.write(f"MCF Rates File: {mcf_filename}\n")
        file.write(f"Optimal MCF Rate: {optimal_mcf}\n")
        file.write("\n")
        file.write(f"Calculated Robustness Measure: {robustness_measure}\n")

if __name__ == "__main__":
    main()
