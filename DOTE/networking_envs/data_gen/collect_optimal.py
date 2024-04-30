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
    # do this on a file by file basis
    hist_name = args[0]
    train_test = args[1]
    props = parse_args(args[2:])

    print(f"hist_name: {hist_name}")
    print(f"train_test: {train_test}")
    print(f"props: {props}")
    
    base_folder = "%s/%s/"%(props.hist_location, props.ecmp_topo)
    
    fname = "%s/%s/%s"%( base_folder, train_test, hist_name)
    
    tms = SLU.get_data([fname], None)

    print(tms)
    
    ############################
    # do regualr
    tunnel_frac = []
    opt_res = []
    for i, tm in enumerate(tqdm(tms)):
        res_str = DGU.get_opt_cplex(props, tm)
        tunnels, opt = output_to_routing(res_str)
        tunnel_frac.append(tunnels)
        opt_res.append(opt)
             
    with open(fname +".opt", 'w') as f:
        f.write('\n'.join(opt_res))
    with open(fname +".tunnels", 'w') as f:
        f.write('\n'.join(tunnel_frac))
    
    ############################ 


if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
