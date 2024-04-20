import os
import pickle
import numpy as np
import re
import glob

import pandas as pd

# Configuration values
src_dir = '/home/azureuser/TEBench/traffic-matrices/perturbated/B4'  # Source directory for .hist files
topology = "B4"

# Ensure that the source directory exists
if not os.path.exists(src_dir):
    os.makedirs(src_dir)

# Function to extract numbers from filename for sorting and indexing
def extract_numbers(filename):
    numbers = re.findall(r'\d+', filename)
    return [int(num) for num in numbers] if numbers else [0]

# Function to read .hist file, convert its content to a numpy array
def read_and_convert_hist_file(hist_file_path):
    with open(hist_file_path, 'r') as file:
        data = []
        for line in file:
            line_data = list(map(float, line.strip().split()))
            data.append(line_data)
    return np.array(data)

# Function to save data to a pickle file
def save_to_pkl(data, output_file_path):
    with open(output_file_path, 'wb') as pkl_file:
        pickle.dump(data, pkl_file)

# Function to process directories and convert each row in .hist files to a .pkl file
def process_directory(base_dir, topology):
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.hist'):
                hist_file_path = os.path.join(root, file)
                data_array = read_and_convert_hist_file(hist_file_path)

                for index, row_data in enumerate(data_array):
                    # Filename incorporates the index of the row in the .hist file
                    pkl_file_name = f'{topology}.json_real_{os.path.splitext(file)[0]}_{index}_1.0_traffic-matrix.pkl'
                    output_file_path = os.path.join(root, pkl_file_name)

                    save_to_pkl(pd.DataFrame(row_data), output_file_path)
                    print(f"Converted row {index} of {hist_file_path} to {output_file_path}")

# Run the processing function
process_directory(src_dir, topology)
print(f'All rows in .hist files have been processed and converted to .pkl files in {src_dir}')
