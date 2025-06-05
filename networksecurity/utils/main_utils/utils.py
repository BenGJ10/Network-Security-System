import yaml
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

import dill 
import pickle

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