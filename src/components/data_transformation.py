import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder ,StandardScaler

import os
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object
@dataclass
class DataTransformationConfig:
    preproccesor_obj_file_path = os.path.join('artifacts', "preprocessor.pkl")  # Specifies the file path where the preprocessor object will be saved

class DataTranformation:
    def __init__(self):
        self.data_tranformation_config = DataTransformationConfig()  # Initializes the DataTransformationConfig instance

    def get_data_transformer_object(self):
        '''
        This function is responsible for data transformation
        '''
        try:
            numerical_column =["writing_score", "reading_score"]  # List of numerical columns
            categorical_columns = [  # List of categorical columns
                "gender", 
                "race_ethnicity", 
                "parental_level_of_education", 
                "test_preparation_course" 
            ]

            # Creating a pipeline for numerical columns - handles missing values and scaling
            num_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),  # Replace missing values with the median of the column
                    ("scaler", StandardScaler())  # Standardize the numerical features (mean=0, std=1)
                ]
            )

            # Creating a pipeline for categorical columns - handles missing values, encoding, and scaling
            cat_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),  # Replace missing values with the most frequent value
                    ("onr_hot_encoder", OneHotEncoder()),  # One hot encode the categorical columns
                    ("scaler", StandardScaler(with_mean=False))  # Scale the encoded values without centering (important for one-hot encoding)
                ]
            )

            logging.info(f"categorical columns:{categorical_columns}")  # Log the categorical columns for debugging
            logging.info(f"Numerical columns:{numerical_column}")  # Log the numerical columns for debugging

            # ColumnTransformer applies the respective pipelines to numerical and categorical columns
            preprocessor = ColumnTransformer(
                [
                    ("num_pipeline", num_pipeline, numerical_column),  # Apply num_pipeline to numerical columns
                    ("cat_pipeline", cat_pipeline, categorical_columns)  # Apply cat_pipeline to categorical columns
                ]
            )

            return preprocessor  # Return the preprocessor object to be used for transformations
        except Exception as e:
            raise CustomException(e, sys)  # Handle any exceptions that occur during the preprocessing setup

    def initiate_data_transformation(self, train_path, test_path):  # Function to initiate data transformation
        try:
            # Read the training and test datasets into pandas DataFrames
            train_df = pd.read_csv(train_path)  # Load the training data from the provided path
            test_df = pd.read_csv(test_path)  # Load the test data from the provided path

            logging.info("Read train and test data complete")  # Log that the data has been read successfully

            logging.info("Obtaining preprocessing object")  # Log that we're getting the preprocessor object
            preprocessor_obj = self.get_data_transformer_object()  # Get the preprocessor object

            target_column = "math_score"  # The target column (the variable we are trying to predict)
            numerical_column = ["writing_score", "reading_score"]  # List of numerical columns to be used as features

            # Separate the input features (X) and target variable (y) for training data
            input_feature_train_df = train_df.drop(columns=[target_column], axis=1)  # Drop the target column to get input features
            target_feature_train_df = train_df[target_column]  # Extract the target column (math_score) for training data

            # Separate the input features (X) and target variable (y) for test data
            input_feature_test_df = test_df.drop(columns=[target_column], axis=1)  # Drop the target column to get input features for test data
            target_feature_test_df = test_df[target_column]  # Extract the target column (math_score) for test data

            logging.info("Applying preprocessing object on training dataframe and test dataframe")  # Log that we're applying the preprocessing steps

            # Apply the preprocessor transformations to the input features (fit on training data and transform on both train and test)
            input_feature_train_arr = preprocessor_obj.fit_transform(input_feature_train_df)  # Fit and transform the training features
            input_feature_test_arr = preprocessor_obj.transform(input_feature_test_df)  # Only transform the test features (using the same preprocessor)

            # Combine the transformed features and target variables for both train and test datasets
            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]  # Concatenate transformed features and target for training data
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]  # Concatenate transformed features and target for test data

            # Save the preprocessor object to a file for future use (i.e., applying the same transformations to new data)
            save_object(
                file_path=self.data_tranformation_config.preproccesor_obj_file_path,  # The file path where the preprocessor object will be saved
                obj=preprocessor_obj  # The preprocessor object that contains all the transformation logic
            )

            # Return the transformed training and test arrays along with the file path where the preprocessor object was saved
            return (
                train_arr,
                test_arr,
                self.data_tranformation_config.preproccesor_obj_file_path  # Return the preprocessor file path
            )
        except Exception as e:
            raise CustomException(e, sys)  # Handle any exceptions that occur during data transformation
