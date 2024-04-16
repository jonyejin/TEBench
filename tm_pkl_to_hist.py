import pandas as pd
import os
import glob
import numpy as np
import re

# Configuration values
src_dir = 'TEAL/traffic-matrices/toy/Kdl'  # Directory where .pkl files are located
dest_dir = 'DOTE/networking_envs/data/Kdl'  # Directory to save the .hist files

# Function to extract number from filename for sorting
def extract_numbers(filename):
    numbers = re.findall(r'\d+', filename)
    return [int(num) for num in numbers] if numbers else [0]

# Create the output directories if they don't exist
if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)
train_dir = os.path.join(dest_dir, 'train')
test_dir = os.path.join(dest_dir, 'test')
os.makedirs(train_dir, exist_ok=True)
os.makedirs(test_dir, exist_ok=True)

# Find all .pkl files in the source directory and sort them numerically
pkl_files = glob.glob(os.path.join(src_dir, '*.pkl'))
pkl_files_sorted = sorted(pkl_files, key=extract_numbers)

# Split the files into train and test sets based on the ratio
train_ratio = 0.75
split_index = int(len(pkl_files_sorted) * train_ratio)
train_files = pkl_files_sorted[:split_index]
test_files = pkl_files_sorted[split_index:]
print(test_files)

# Function to convert data to .hist files
def convert_to_hist(files, output_dir):
    for file_path in files:
        data = pd.read_pickle(file_path)  # Load the .pkl file

        # Check if the data is a DataFrame or a numpy array
        if isinstance(data, pd.DataFrame):
            rows = data.iterrows()
        elif isinstance(data, np.ndarray):
            rows = enumerate(data)

        # Extract the file name and change the extension to .hist
        base_name = os.path.basename(file_path)
        hist_file_name = os.path.splitext(base_name)[0] + '.hist'

        # Save the data as a .hist file
        output_path = os.path.join(output_dir, hist_file_name)
        with open(output_path, 'w') as f:
            for index, row in rows:
                f.write(' '.join(map(str, row)) + '\n')

# Convert and save the .pkl files as .hist files in the respective train and test directories
convert_to_hist(train_files, train_dir)
convert_to_hist(test_files, test_dir)

print(f'{len(train_files)} pkl files have been converted to hist files in {train_dir}')
print(f'{len(test_files)} pkl files have been converted to hist files in {test_dir}')
