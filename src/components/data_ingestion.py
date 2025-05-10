import os     # for using exception and logging
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.components.data_transformation import DataTranformation
from src.components.data_transformation import DataTransformationConfig

from src.components.model_trainer import ModelTrainer
from src.components.model_trainer import ModelTrainerConfig

# The DataIngestionConfig class uses the @dataclass decorator to automatically generate special methods
# such as __init__, __repr__, and __eq__ based on the class attributes.
@dataclass
class DataIngestionConfig:
    # Path where the training data will be saved (as CSV).
    train_data_path: str = os.path.join('artifacts', "train.csv")
    # Path where the testing data will be saved (as CSV).
    test_data_path: str = os.path.join('artifacts', "test.csv")
    # Path where the raw data will be saved (as CSV).
    raw_data_path: str = os.path.join('artifacts', "raw.csv")

# The DataIngestion class is responsible for the entire data ingestion process.
class DataIngestion:
    def __init__(self):        # The constructor initializes the ingestion configuration by creating an instance of DataIngesttionConfig.
        self.ingestion_config = DataIngestionConfig()   # Creates an instance of DataIngesttionConfig containing the paths for saving data.
    
    def initiate_data_ingestion(self):         # This method handles the data ingestion process — reading the data, splitting it, and saving it.

        logging.info("Enter the data ingestion method or component")
        try:
            # Read the dataset from a CSV file into a pandas DataFrame.
            df = pd.read_csv("notebook\\data\\stud.csv")
            # Logging to confirm that the dataset has been successfully read into the DataFrame.
            logging.info("Read the dataset as DataFrame")
            
            # Create directories for the train data path if they don't already exist.
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)

            # Save the raw dataset to the specified raw data path (raw.csv).
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

            logging.info("Train test split initiated")
            # Split the data into 80% training set and 20% test set.
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=32)

            # Save the training data to the train data path (train.csv).
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)

            # Save the test data to the test data path (test.csv).
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            logging.info("Ingestion is now complete")

            # Return the file paths of the train and test data.
            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        except Exception as e:
            # If any exception occurs, pass it to the CustomException for logging and handling.
            CustomException(e, sys)

# Main method to execute the DataIngestion class.
if __name__ == "__main__":
    obj = DataIngestion()               # Instantiate the DataIngestion class.
    train_data, test_data = obj.initiate_data_ingestion()       # Call the method to start the data ingestion process.

    data_transforamtion = DataTranformation()
    train_arr , test_arr ,_ = data_transforamtion.initiate_data_transformation(train_data ,test_data)

    model_trainer =ModelTrainer()
    print(model_trainer.initiate_model_trainer(train_arr , test_arr))
