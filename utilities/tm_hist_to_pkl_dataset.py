import os
import pickle
import pandas as pd
import numpy as np

dataset = "Abilene"
def process_directory(directory, output_directory, start_index=0):
    """Process all .hist files in a directory, saving each row as a separate .pkl file."""
    current_index = start_index
    for root, _, files in sorted(os.walk(directory)):
        for file in sorted(files):
            if file.endswith('.hist'):
                hist_file_path = os.path.join(root, file)
                with open(hist_file_path, 'r') as hist_file:
                    for line_number, line in enumerate(hist_file, 1):
                        line_data = list(map(float, line.strip().split()))
                        if not line_data:
                            continue
                        output_file_name = f"{dataset}.json_real_{current_index+1}_1.0_traffic-matrix.pkl"
                        output_file_path = os.path.join(output_directory, output_file_name)

                        line_data = np.array(line_data)
                        length = len(line_data)
                        if int(np.sqrt(length)) ** 2 != length:
                            raise ValueError(
                                "The number of elements is not a perfect square, cannot reshape into a square array.")

                        square_size = int(np.sqrt(length))
                        square_array = line_data.reshape((square_size, square_size))

                        save_to_pkl(square_array, output_file_path)
                        print(square_array)
                        print(f"Saved {output_file_path}")
                        current_index += 1
    return current_index

def save_to_pkl(data, output_file_path):
    """Save data to a pickle file."""
    with open(output_file_path, 'wb') as pkl_file:
        print(output_file_path)
        pickle.dump(data, pkl_file)

# Define the directories and output directory
train_dir = f'/Users/yejin/TEBench/DOTE/networking_envs/data/{dataset}/train'
test_dir = f'/Users/yejin/TEBench/DOTE/networking_envs/data/{dataset}/test'
output_dir = f'/Users/yejin/TEBench/TEAL/traffic-matrices/real'

# Process the directories and save each row as a separate .pkl file
last_index_train = process_directory(train_dir, output_dir)
process_directory(test_dir, output_dir, last_index_train)
