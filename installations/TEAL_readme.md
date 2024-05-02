### TEAL - uses conda environment named “TEAL”
```bash
cd TEAL
git submodule update --init --recursive
```

```bash
conda env create -f environment.yml --name TEAL
pip install -r requirements.txt 
```
```bash
sudo apt install build-essential -y
```
### check CUDA version
```bash
nvcc --version # 11.5
```
### installation based on nvcc 11.5 

### remove colliding packages
```bash
conda remove libstdcxx-ng
conda install libgcc-ng>=9.4.0

conda install pytorch=1.11.0 torchvision torchaudio cudatoolkit=11.5 -c pytorch -c nvidia

pip install scipy
pip install --no-index torch-scatter torch-sparse -f https://data.pyg.org/whl/torch-1.11.0%2Bcu115.html

python -c "import torch_scatter; print(torch_scatter.__version__)" #2.0.9
python -c "import torch_sparse; print(torch_sparse.__version__)" # 0.6.15

conda install networkx
conda install tqdm
```
