import pickle

def read_hist_file(hist_file_path):
    data = []
    with open(hist_file_path, 'r') as file:
        for line in file:
            # Convert each line to a list of floats
            line_data = list(map(float, line.strip().split()))
            data.append(line_data)
    return data

def save_to_pkl(data, output_file_path):
    with open(output_file_path, 'wb') as pkl_file:
        pickle.dump(data, pkl_file)

def convert_hist_to_pkl(hist_file_path, pkl_file_path):
    data = read_hist_file(hist_file_path)
    save_to_pkl(data, pkl_file_path)

# Example usage
hist_file_path = '2.hist'
pkl_file_path = 'Abilene.json_toy_2_1.0_traffic-matrix.pkl'
convert_hist_to_pkl(hist_file_path, pkl_file_path)
