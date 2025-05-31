import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging


# Configuration of Data Ingestion 
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact
import numpy as np
import pandas as pd
import certifi
import pymongo
from pymongo.server_api import ServerApi
from sklearn.model_selection import train_test_split

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

class DataIngestion:
    """
    DataIngestion class is responsible for ingesting data from a MongoDB database,
    processing it, and exporting it into a feature store as well as splitting it into
    training and testing datasets. It handles the connection to the database,
    retrieves the data, and manages the file paths for the feature store and datasets.
    """
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def export_collection_as_dataframe(self):
        """Read data from MongoDB database.\n
        This function connects to the MongoDB database using the provided URL,
        retrieves the specified collection, and converts it into a pandas DataFrame.
        It also handles the removal of the "_id" column if it exists in the DataFrame."
        """

        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            logging.info("Connecting to the MongoDB database...")
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL, server_api = ServerApi('1'), tls = True, tlsCAFile = certifi.where())
            collection = self.mongo_client[database_name][collection_name]
            df = pd.DataFrame(list(collection.find()))
            
            if "_id" in df.columns.tolist():
                df = df.drop(columns = ["_id"], axis = 1)

            df.replace({"na" : np.nan}, inplace = True)
            logging.info("Data retrieved from MongoDB database.")
            return df

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def export_data_to_feature_store(self, dataframe: pd.DataFrame):
        """ Export data retrieved from MongoDB database into csv format.
        This function creates a directory for the feature store file if it does not exist,
        and saves the dataframe as a CSV file in that directory.
        """
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            # Creating a folder
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok = True)
            dataframe.to_csv(feature_store_file_path, header = True, index = False)
            logging.info("Exported data into csv format.")
            return dataframe
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def export_train_test_split(self, dataframe: pd.DataFrame):
        """Split the dataframe into training and testing datasets."""
        try:
            train_set, test_set = train_test_split(
                dataframe, test_size = self.data_ingestion_config.train_test_split_ratio
            )
            logging.info("Performing train-test split on the dataframe.")

            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok = True)

            train_set.to_csv(
                self.data_ingestion_config.training_file_path, index = False, header = True
            )
            test_set.to_csv(
                self.data_ingestion_config.testing_file_path, index = False, header = True
            )
            logging.info("Exported training and testing file path.")

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_ingestion(self):
        """Initiate the data ingestion process."""
        try:
            logging.info("Starting data ingestion process...")
            dataframe = self.export_collection_as_dataframe()
            dataframe = self.export_data_to_feature_store(dataframe)
            self.export_train_test_split(dataframe)

            data_ingestion_artifact = DataIngestionArtifact(train_file_path = self.data_ingestion_config.training_file_path,
                                                            test_file_path = self.data_ingestion_config.testing_file_path)            
            return data_ingestion_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)