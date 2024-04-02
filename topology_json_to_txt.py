import json
import numpy as np
def json_to_adjacency_matrix(json_data):
    node_ids = [node['id'] for node in json_data['nodes']]
    n = max(node_ids) + 1  # Determine the matrix size
    adj_matrix = np.zeros((n, n), dtype=float)  # Initialize the adjacency matrix

    # Populate the adjacency matrix with capacities
    for link in json_data['links']:
        source = link['source']
        target = link['target']
        capacity = link['capacity']
        adj_matrix[source, target] = capacity

    # Convert the adjacency matrix to a string format for saving to .txt file
    matrix_str = '\n'.join(','.join(str(adj_matrix[source, target])
                                   for target in range(n))
                           for source in range(n))
    return matrix_str

json_data = json.loads(open('TEAL/topologies/B4.json', 'r').read())

# Convert the JSON data to adjacency matrix string
adj_matrix_str = json_to_adjacency_matrix(json_data)

with open("DOTE/networking_envs/data/B4_Zoe/B4_int.txt", 'w') as file:
    file.write(adj_matrix_str)

