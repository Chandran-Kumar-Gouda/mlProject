import sys
import os
import dill

import pandas as pd 
import numpy as np
from src.exception import CustomException
def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)  # Extracts the directory part of the given file path.

        os.makedirs(dir_path, exist_ok=True)  # Creates the directory if it doesn’t exist, ignoring errors if the directory already exists.

        with open(file_path, "wb") as file_obj:  # Opens the file in write-binary mode to store the object.
            dill.dump(obj, file_obj)  # Serializes and saves the Python object into the file using dill.
    
    except Exception as e:
        raise CustomException(e,sys)