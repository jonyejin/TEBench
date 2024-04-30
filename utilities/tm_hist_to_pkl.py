import os
import pickle
import numpy as np
import re
import glob
import pandas as pd

# Root directory for all topology data
root_dir = '/home/azureuser/TEBench/traffic-matrices/perturbated'

# Ensure that the root directory exists
if not os.path.exists(root_dir):
    os.makedirs(root_dir)

# Function to delete existing .pkl files in a directory
def delete_existing_pkl_files(directory):
    for pkl_file in glob.glob(os.path.join(directory, '*.pkl')):
        os.remove(pkl_file)
        print(f"Deleted existing file: {pkl_file}")

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
            if line_data:  # Ensure the line has data
                data.append(line_data)
    return np.array(data)

# Function to save data to a pickle file
def save_to_pkl(data, output_file_path):
    if data.size > 0:  # Check if the data array is not empty
        with open(output_file_path, 'wb') as pkl_file:
            pickle.dump(data, pkl_file)
        print(f"Saved file: {output_file_path}")
    else:
        print(f"No data to save for {output_file_path}")

# Function to process directories and convert each row in .hist files to a .pkl file
def process_directory(base_dir):
    for root, dirs, files in os.walk(base_dir):
        delete_existing_pkl_files(root)  # Delete existing .pkl files in the directory
        topology = root.split(os.sep)[-3]  # Assumes that topology name is three levels up from the files
        for file in files:
            if file.endswith('.hist'):
                hist_file_path = os.path.join(root, file)
                data_array = read_and_convert_hist_file(hist_file_path)

                for index, row_data in enumerate(data_array):
                    pkl_file_name = f'{topology}.json_real_{index}_1.0_traffic-matrix.pkl'
                    output_file_path = os.path.join(root, pkl_file_name)
                    save_to_pkl(pd.DataFrame(row_data), output_file_path)

# Run the processing function for all subdirectories under the root directory
process_directory(root_dir)
print(f'All rows in .hist files have been processed and converted to .pkl files in all subdirectories under {root_dir}')
