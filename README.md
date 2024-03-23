# BV - binocular vision toolkits

This repository is designed to quick-start binocular vision related works.



## QuickStart

Virtual environments such as anaconda is recommended for using bv-toolkits.

> To download anaconda, refer to: [Free Download | Anaconda](https://www.anaconda.com/download/)
>
> Note: look up a related tutorial to set up a virtual environment.

Use commands as follows to create your python running environment:

```bash
# make sure you are in the root path of binocular_vision

# <env_name> should be replaced with your preferred name
# <linux|windows> should be chosen for your platform

conda init # (if needed)

conda create --name <env_name> --file .ci/conda_env_<linux|windows>.txt

conda activate <env_name>

pip install -r .ci/py_requirements_<linux|windows>.txt
```

To run a tutorial, use command like:

```bash
cd tutorial

# linux
./tutor_stereo_calib.py

# windows
python3.exe ./tutor_stereo_calib.py
```



## Note

### New Python Module

If any new python module is added to this project, use command as follows to update related env:

```bash
# for conda
conda list --export > .ci/conda_env_<linux|windows>.txt

# for pip
pip freeze > .ci/py_requirements_<linux|windows>.txt
```