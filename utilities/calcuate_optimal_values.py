from pathlib import Path

import os
from tqdm import tqdm
import argparse

from networking_envs.data_gen import utils as DGU
from networking_envs.ml.sl_algos import utils as SLU
from networking_envs.networking_env.environments.ecmp.env_args_parse import parse_args as custom_parse_args

def output_to_routing(res):
    if isinstance(res, list):
        res = '\n'.join(res)

    for line in res.split("\n"):
        if "Optimal result for actual demand:" in line:
            opt_res = line.split(":")[1].strip()
            print(opt_res)
            return None, opt_res

def main(args):
    # Usage should be like:
    # test.hist test --ecmp_topo B4 --opt_function MAXCONC
    hist_file_name = args[0]
    train_test = args[1]
    specific_dir = args[2]

    props = custom_parse_args(args[3:])

    if specific_dir.__contains__("perturbated"):
        fname = Path(f"../traffic-matrices/{specific_dir}/{hist_file_name}/")
    else:
        fname = Path(f"../traffic-matrices/{specific_dir}/{props.ecmp_topo}/{train_test}/{hist_file_name}/")

    tms = SLU.get_data([fname], None)

    opt_res = []
    for i, tm in enumerate(tqdm(tms)):
        res_str = DGU.get_opt_cplex(props, tm)
        _, opt = output_to_routing(res_str)
        opt_res.append(opt)
    output_file_name = str(fname)[:-5] + "_" + props.opt_function + ".opt"
    with open(output_file_name, 'w') as f:
        f.write('\n'.join(opt_res))

    print(f"saved at {output_file_name}")

if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
