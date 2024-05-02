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

    print(res)

    for line in res.split("\n"):
        if "Optimal result for actual demand:" in line:
            opt_res = line.split(":")[1].strip()
            print(opt_res)
            return None, opt_res


def main(args):
    # should be like
    # test.hist test --ecmp_topo B4 --opt_function MAXCONC
    hist_file_name = args[0]
    train_test = args[1]
    props = custom_parse_args(args[2:])

    print(f"hist_name: {hist_file_name}")
    print(f"train_test: {train_test}")
    print(f"props: {props}")

    fname = Path(f"../traffic-matrices/original/{props.ecmp_topo}/{train_test}/{hist_file_name}/")
    tms = SLU.get_data([fname], None)

    tunnel_frac = []
    opt_res = []
    for i, tm in enumerate(tqdm(tms)):
        res_str = DGU.get_opt_cplex(props, tm)
        tunnels, opt = output_to_routing(res_str)
        tunnel_frac.append(tunnels)
        opt_res.append(opt)

    with open(fname + ".opt", 'w') as f:
        f.write('\n'.join(opt_res))
    with open(fname + ".tunnels", 'w') as f:
        f.write('\n'.join(tunnel_frac))


if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
