from networking_env.environments.ecmp.env_args_parse import parse_args

import os
from tqdm import tqdm

from data_gen import utils as DGU
from ml.sl_algos import utils as SLU


def output_to_routing(res):
    if isinstance(res, list):
        res = '\n'.join(res)

    print(res)

    for line in res.split("\n"):
        if "Optimal result for actual demand:" in line:
            opt_res = line.split(":")[1].strip()
            print(opt_res)
            return None, opt_res


def main(args):
    props = parse_args(args)

    # Define fname directly to use a specific file path
    fname = "/Users/yejin/TEBench/traffic-matrices/perturbated/Abilene/Gaussian_Multiplicative_Noise/0.4/test.hist"

    # Load traffic matrices
    tms = SLU.get_data([fname], None)

    # print(tms)

    # Initialize results lists
    # tunnel_frac = []
    opt_res = []

    # Process each traffic matrix
    for i, tm in enumerate(tqdm(tms)):
        # Call get_opt_cplex with appropriate settings
        res_str = DGU.get_opt_cplex(props, tm, use_cplex=False)  # Example: Assuming use_cplex=True here
        _, opt = output_to_routing(res_str)
        # tunnel_frac.append(tunnels)
        opt_res.append(opt)

    # Write optimization results to files
    with open(fname + ".opt", 'w') as f:
        f.write('\n'.join(opt_res))
    # with open(fname + ".tunnels", 'w') as f:
    #     f.write('\n'.join(tunnel_frac))


if __name__ == "__main__":
    import sys

    main(sys.argv[1:])
