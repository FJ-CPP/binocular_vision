# BV - binocular vision toolkits

This repository is designed to quick-start binocular vision related works.



## QuickStart

Virtual environments such as anaconda is recommended for using bv-toolkits.

> To download anaconda, refer to: [Free Download | Anaconda](https://www.anaconda.com/download/)
>
> Note: look up a related tutorial to set up a virtual environment.

1. Use commands as follows to create your python running environment:

```bash
# make sure you are in the root path of binocular_vision

conda init # (if needed)

conda env create -f .ci/conda_env_linux.yaml

conda activate bv

pip install -r .ci/py_requirements_linux.txt

# for raft-stereo, CUDA 11.3 is needed

cd 3rdparties/RAFT-Stereo/sampler

python setup.py install
```
2. Download needed datasets
```bash
# for linux
download_datasets.sh
```
3. To run a tutorial, use command like:

```bash
cd tutorial

./tutor_stereo_calib.py
```



## Note

### New Python Module

If any new python module is added to this project, use command as follows to update related env:

```bash
# for conda
conda env export > .ci/conda_env_linux.yaml

# for pip
pip freeze > .ci/py_requirements_linux.txt
```