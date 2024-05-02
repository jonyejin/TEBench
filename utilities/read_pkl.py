import pickle

import pandas as pd
import os


def load_pkl_files(filename):
    """Loads all .pkl files from the specified directory and prints their contents."""
    with open(filename, 'rb') as f:
        df = pickle.load(f)
        print(type(df))
        print(f"Contents of {filename}:")
        print(df)
    print("\n")  # Print a newline for better separation between files


current_dir = os.getcwd()
index_dote = current_dir.find("TEBench")
if index_dote != -1:
    base_path = current_dir[:index_dote]

load_pkl_files(f"{base_path}TEAL/traffic-matrices/toy/ASN2k.json_toy_0_1.0_traffic-matrix.pkl")
