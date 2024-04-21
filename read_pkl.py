import pickle

import pandas as pd
import os

def load_pkl_files(filename):
    """Loads all .pkl files from the specified directory and prints their contents."""
    with open(filename, 'rb') as f:
        df = pickle.load(f)
        print(f"Contents of {filename}:")
        print(df)
    print("\n")  # Print a newline for better separation between files

# Specify the directory containing your .pkl files
# Load and display the contents of all .pkl files in the specified directory
# load_pkl_files( "/home/azureuser/TEBench/traffic-matrices/perturbated/B4/Gaussian_Multiplicative_Noise/0.2/B4.json_real_test_9_1.0_traffic-matrix.pkl")
load_pkl_files( "/home/azureuser/TEBench/TEAL/traffic-matrices/real/GEANT.json_real_139_1.0_traffic-matrix.pkl")
