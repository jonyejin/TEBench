import os
import glob
import subprocess
import argparse
import shutil

def compute_opts(topology_name):
    opts_dir_prefix = 'opts_'
    paths_from = 'sp'

    test_opts_dir = opts_dir_prefix + 'test'
    train_opts_dir = opts_dir_prefix + 'train'

    if os.path.exists(test_opts_dir):
        shutil.rmtree(test_opts_dir)
    if os.path.exists(train_opts_dir):
        shutil.rmtree(train_opts_dir)

    os.mkdir(test_opts_dir)
    os.mkdir(train_opts_dir)

    subprocess.run(
        ['python', '../../ml/sl_algos/evaluate.py', '--ecmp_topo', topology_name, '--hist_len', '0', '--sl_type',
         'stats_comm', '--compute_opts', '--paths_from', paths_from, '--opt_function', 'MAXCONC'], check=True)
    subprocess.run(
        ['python', '../../ml/sl_algos/evaluate.py', '--ecmp_topo', topology_name, '--hist_len', '0', '--sl_type',
         'eval', '--compute_opts', '--opts_dir', test_opts_dir, '--opt_function', 'MAXCONC'], check=True)

    subprocess.run(
        ['python', '../../ml/sl_algos/evaluate.py', '--ecmp_topo', topology_name, '--hist_len', '0', '--sl_type',
         'stats_comm', '--compute_opts', '--compute_opts_dir', 'train', '--opt_function', 'MAXCONC'], check=True)
    subprocess.run(
        ['python', '../../ml/sl_algos/evaluate.py', '--ecmp_topo', topology_name, '--hist_len', '0', '--sl_type',
         'eval', '--compute_opts', '--compute_opts_dir', 'train', '--opts_dir', train_opts_dir, '--opt_function', 'MAXCONC'], check=True)

    for d in ['test', 'train']:
        opts_info = []
        for file in sorted(glob.glob(d + "/*.hist")):
            with open(file) as f:
                opts_info.append((file[:-4] + 'opt', len(f.readlines())))

        input_file_idx = 0
        for i in range(len(opts_info)):
            opt_res_for_actual_demands = []
            for j in range(opts_info[i][1]):
                input_file_name = str(input_file_idx) + '.opt'
                with(open(opts_dir_prefix + d + '/' + input_file_name)) as f:
                    lines = f.read().splitlines()
                    for line in lines:
                        if line.startswith(' Optimal result for actual demand: '):
                            opt_res = float(line[line.find(': ') + 1:])
                            opt_res_for_actual_demands.append(opt_res)

                input_file_idx += 1

            with open(opts_info[i][0], 'w') as f:
                for o in opt_res_for_actual_demands:
                    f.write(str(o) + '\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some parameters.')
    parser.add_argument('--topology', type=str, help='Name of the topology')

    args = parser.parse_args()

    if args.topology:
        compute_opts(args.topology)
    else:
        print("No topology name provided.")
