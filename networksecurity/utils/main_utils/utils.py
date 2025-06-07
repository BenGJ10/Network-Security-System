import yaml
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

import pickle
import numpy as np

def read_yaml_file(file_path: str) -> dict:
    """
    Reads a YAML file and returns its contents as a dictionary.
    """
    try:
        with open(file_path, 'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e
    
def write_yaml_file(file_path: str, content: object, replace:  bool = False) -> None:
    """
    Writes a dictionary to a YAML file. If the file already exists and replace is True, it will overwrite the file.
    If the file does not exist, it will create the necessary directories and write the file."""
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok = True)    
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
def save_numpy_array(file_path: str, array: np.array):
    """
    Saves a NumPy array to a specified file path using np.save.
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok = True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
def save_object(file_path: str, obj: object) -> None:
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok = True)
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
        logging.info("Successfully saved the pkl object")
    except Exception as e:
        raise NetworkSecurityException(e, sys)