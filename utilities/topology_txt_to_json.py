import csv
import json
import networkx as nx

topology = "Abilene"
def read_matrix_from_file(filename):
    """Read a matrix from a CSV file and return it as a list of lists."""
    matrix = []
    with open(filename, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            matrix.append([float(value) if value else 0.0 for value in row])
    return matrix

def create_graph_from_matrix(matrix):
    """Create a directed graph and add edges in both directions for each connection."""
    G = nx.DiGraph()
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] != 0:
                # Add edge in the forward direction
                G.add_edge(i, j, capacity=matrix[i][j])
                # Add edge in the backward direction
                G.add_edge(j, i, capacity=matrix[i][j])
    return G

def save_graph_to_file(graph, filename):
    """Save the graph to a file in JSON format."""
    data = nx.node_link_data(graph)  # Convert the graph to node-link format data
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

# Read the matrix from a file
matrix = read_matrix_from_file(f'../DOTE/networking_envs/data/{topology}/{topology}_int.txt')

# Create a graph from the matrix
graph = create_graph_from_matrix(matrix)

# Save the graph to a file
save_graph_to_file(graph, f'../TEAL/topologies/{topology}.json')
