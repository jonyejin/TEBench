import os
import pickle
import pandas as pd

dataset = "GEANT"
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
                        save_to_pkl(pd.DataFrame(line_data), output_file_path)
                        print(f"Saved {output_file_path}")
                        current_index += 1
    return current_index

def save_to_pkl(data, output_file_path):
    """Save data to a pickle file."""
    with open(output_file_path, 'wb') as pkl_file:
        pickle.dump(data, pkl_file)

# Define the directories and output directory
train_dir = '/home/azureuser/TEBench/DOTE/networking_envs/data/GEANT/train'
test_dir = '/home/azureuser/TEBench/DOTE/networking_envs/data/GEANT/test'
output_dir = '/home/azureuser/TEBench/TEAL/traffic-matrices/real'

# Process the directories and save each row as a separate .pkl file
last_index_train = process_directory(train_dir, output_dir)
process_directory(test_dir, output_dir, last_index_train)
