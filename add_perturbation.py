import numpy as np

def add_noise_to_traffic(tms, a):
    """
    Add noise to traffic matrices by multiplying each demand with a factor
    sampled uniformly from [1-a, 1+a].

    :param tms: Traffic matrices, a numpy array of shape (num_matrices, num_nodes, num_nodes).
    :param a: The perturbation factor.
    :return: A new numpy array with perturbed traffic matrices.
    """
    # For each element in the traffic matrices, multiply by a random factor within [1-a, 1+a]
    noise_factors = np.random.uniform(1 - a, 1 + a, tms.shape)
    perturbed_tms = tms * noise_factors
    return perturbed_tms

# Example usage
a_values = [0.1, 0.25, 0.35]
test_traffic_matrices = np.random.rand(100, 12, 12)  # Assuming 100 matrices for a 12-node network

# Apply noise to the test set for each 'a' value
for a in a_values:
    perturbed_test_tms = add_noise_to_traffic(test_traffic_matrices, a)
    print(f"Perturbed traffic matrices for a={a} have been generated.")
