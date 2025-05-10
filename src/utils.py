import sys
import os
import dill

import pandas as pd 
import numpy as np
from src.exception import CustomException
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path)  # Extracts the directory part of the given file path.

        os.makedirs(dir_path, exist_ok=True)  # Creates the directory if it doesn’t exist, ignoring errors if the directory already exists.

        with open(file_path, "wb") as file_obj:  # Opens the file in write-binary mode to store the object.
            dill.dump(obj, file_obj)  # Serializes and saves the Python object into the file using dill.
    
    except Exception as e:
        raise CustomException(e,sys)
    
def evaluate_model(X_train ,y_train ,X_test ,y_test ,models,param):
    try:
        reports ={}

        for i in range(len(list(models))):
            model =list(models.values())[i]
# Get the corresponding hyperparameter grid from the `param` dictionary for the current model
            para = param[list(models.keys())[i]] 

# Create a GridSearchCV object to search for the best combination of hyperparameters using 3-fold cross-validation
            gs = GridSearchCV(model, para, cv=3)

# Fit GridSearchCV on the training data — this will try all combinations in the grid and select the best one
            gs.fit(X_train, y_train)

# Set the model’s parameters to the best combination found by GridSearchCV so we can retrain it on full training data
            model.set_params(**gs.best_params_)

            model.fit(X_train,y_train)
            model.fit(X_train ,y_train)

            y_train_pred = model.predict(X_train)

            y_test_pred = model.predict(X_test)

            train_model_score = r2_score(y_train , y_train_pred)
            test_model_score = r2_score(y_test , y_test_pred)

            reports[list(models.keys())[i]] = test_model_score

        return reports

    except Exception as e:
        raise CustomException(e, sys)

def load_object(file_path):
    try:
        with open(file_path ,"rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        CustomException(e,sys)