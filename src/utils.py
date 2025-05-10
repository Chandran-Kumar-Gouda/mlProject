import sys
import os
import dill

import pandas as pd 
import numpy as np
from src.exception import CustomException
from sklearn.metrics import r2_score
def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)  # Extracts the directory part of the given file path.

        os.makedirs(dir_path, exist_ok=True)  # Creates the directory if it doesn’t exist, ignoring errors if the directory already exists.

        with open(file_path, "wb") as file_obj:  # Opens the file in write-binary mode to store the object.
            dill.dump(obj, file_obj)  # Serializes and saves the Python object into the file using dill.
    
    except Exception as e:
        raise CustomException(e,sys)
    
def evaluate_model(X_train ,y_train ,X_test ,y_test ,models):
    try:
        reports ={}

        for i in range(len(list(models))):
            model =list(models.values())[i]

            model.fit(X_train ,y_train)

            y_train_pred = model.predict(X_train)

            y_test_pred = model.predict(X_test)

            train_model_score = r2_score(y_train , y_train_pred)
            test_model_score = r2_score(y_test , y_test_pred)

            reports[list(models.keys())[i]] = test_model_score

        return reports

    except Exception as e:
        raise CustomException(e, sys)