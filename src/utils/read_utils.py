import json
import yaml
import os
import gzip
import pickle
import numpy as np

def save_yaml(yaml_path:str,data:dict):
    with open(yaml_path, 'w') as outfile:
        yaml.dump(data, outfile, default_flow_style=False)

def read_yaml(yaml_path:str):
    with open(yaml_path) as fd:
        dict = yaml.load(fd, Loader=yaml.SafeLoader)
    return dict

def save_json(json_path:str,data:dict):
    with open(json_path, 'w') as fp:
        json.dump(data, fp)

def read_json(json_path: str) -> dict:
    """
    Reads a json file.

    Args:
        json_path: path to json file

    Returns:
        dict
    """
    if os.path.isfile(json_path):
        with open(json_path, encoding="utf-8") as jfile:
            jdict = json.load(jfile)
        return jdict
    else:
        raise FileNotFoundError(json_path)
    
def read_npy_gz(path:str):
    """Access file in .npy.gz format
    """
    f = gzip.GzipFile(path, "r")
    n = np.load(f)
    return n

def read_pkl_gz(path:str):
    with gzip.open(os.path.join(path), 'rb') as f:
        pkl_obj = pickle.load(f)
    return pkl_obj