import pandas as pd
import os
import glob
import numpy as np
import re

# Configuration values
src_dir_1 = 'DOTE/networking_envs/data/Abilene/train'
src_dir_2 = 'DOTE/networking_envs/data/Abilene/test'
dest_dir = 'TEAL/traffic-matrices/real'
topology = 'Abilene'

# Create the output directory if it doesn't exist
if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)

# Function to extract number from filename for sorting and indexing
def extract_numbers(filename):
    numbers = re.findall(r'\d+', filename)
    return [int(num) for num in numbers] if numbers else [0]

# Function to find and sort .hist files from multiple directories
def find_and_sort_hist_files(*directories):
    hist_files = []
    for directory in directories:
        hist_files += glob.glob(os.path.join(directory, '*.hist'))
    return sorted(hist_files, key=extract_numbers)

# Gather all .hist files from both directories
all_hist_files = find_and_sort_hist_files(src_dir_1, src_dir_2)

# Function to convert .hist files to individual .pkl files
def convert_to_individual_pkl(files, output_dir):
    for file_path in files:
        with open(file_path, 'r') as f:
            lines = f.readlines()

        base_name = os.path.basename(file_path)
        base_index = extract_numbers(base_name)[0]  # Base index from file name

        for i, line in enumerate(lines):
            # Convert the line to a numpy array right away
            data = np.array(list(map(float, line.split())))
            # Create a DataFrame from a numpy array directly, without reshaping
            df = pd.DataFrame(data)

            matrix_order = base_index + i  # Increment index for each line
            pkl_file_name = f'{topology}.json_real_{matrix_order}_1.0_traffic-matrix.pkl'
            output_path = os.path.join(output_dir, pkl_file_name)
            df.to_pickle(output_path)

# Convert and save all .hist files to individual .pkl files in the destination directory
convert_to_individual_pkl(all_hist_files, dest_dir)
print(f'Converted all hist files to individual pkl files in {dest_dir}')
