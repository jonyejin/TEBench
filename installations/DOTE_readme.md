# Setup Guide
This guide provides detailed steps for setting up a virtual environment and installing necessary software on a VM via SSH.

### clone the repository
```bash
git clone https://github.com/PredWanTE/DOTE.git
```

### install python
```bash
sudo apt install python3-pip  -y
```
### install miniconda
```bash
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm -rf ~/miniconda3/miniconda.sh
```
### initialize shells
```bash
~/miniconda3/bin/conda init bash
~/miniconda3/bin/conda init zsh
```
* might have to open new shell here

### create new conda environment
```bash
conda create -n venv python==3.10.12 -y
conda activate venv
conda install -c conda-forge mpi4py mpich -y
```
### install bunch of things
```bash
pip install -r requirements_rl.txt
```
* change tensorflow version from 1.15 to 2.16.1

```bash
pip install scikit-learn
pip3 install networkx==2.8.8
pip3 install torch
pip3 install matplotlib
pip3 install joblib
pip3 install tqdm
```

 
### installing Gurobi Optimizer
```bash
wget https://packages.gurobi.com/9.1/gurobi9.1.2_linux64.tar.gz
tar xvfz gurobi9.1.2_linux64.tar.gz

python -m pip install amplpy --upgrade
python -m amplpy.modules install gurobi
python -m amplpy.modules activate f0369128-85bd-433c-8cfb-cd6c2e3a38fa
```
### set up Gurobi variables
```bash
#!/bin/bash
GUROBI_HOME=~/gurobi912
export GUROBI_HOME
export PATH=$PATH:$GUROBI_HOME/bin
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$GUROBI_HOME/lib

echo "GUROBI_HOME set to $GUROBI_HOME"
echo "PATH set to $PATH"
echo "LD_LIBRARY_PATH set to $LD_LIBRARY_PATH"
```

### git submodules download
```bash
git submodule init
git submodule update
```
### running the code
```bash
cd ~ && conda activate venv && cd TEBench/DOTE/networking_envs/data/B4/ && python3 ../compute_opts.py --topology B4
cd ~ && conda activate DOTE && cd TEBench/DOTE/networking_envs/data/B4/ && python3 ../compute_opts.py --topology B4
```
### updating Gurobi
```bash
python -m pip install gurobipy --upgrade
```