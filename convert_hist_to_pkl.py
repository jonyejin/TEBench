import os
import pickle

def read_hist_file(hist_file_path):
    """Read a .hist file and convert its content to a list of lists of floats."""
    data = []
    with open(hist_file_path, 'r') as file:
        for line in file:
            # Convert each line to a list of floats
            line_data = list(map(float, line.strip().split()))
            data.append(line_data)
    return data

def save_to_pkl(data, output_file_path):
    """Save data to a pickle file."""
    with open(output_file_path, 'wb') as pkl_file:
        pickle.dump(data, pkl_file)

def convert_hist_to_pkl(hist_file_path, pkl_file_path):
    """Convert a .hist file to a .pkl file."""
    data = read_hist_file(hist_file_path)
    save_to_pkl(data, pkl_file_path)

def process_directory(base_dir):
    """Process all .hist files in the directory tree starting at base_dir."""
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.hist'):
                hist_file_path = os.path.join(root, file)
                pkl_file_name = file.replace('.hist', '_traffic-matrix.pkl')
                pkl_file_path = os.path.join(root, pkl_file_name)
                convert_hist_to_pkl(hist_file_path, pkl_file_path)
                print(f"Converted {hist_file_path} to {pkl_file_path}")

# Define the base directory where the .hist files are located
base_dir = '/home/azureuser/TEBench/traffic-matrices/perturbated'

# Call the function to process the directory
process_directory(base_dir)
