import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

# Configuration of Data Validation 
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from scipy.stats import ks_2samp
import pandas as pd
import numpy as np
from networksecurity.constants.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils.main_utils.utils import read_yaml_file, write_yaml_file


class DataValidation:
    """
    DataValidation class is responsible for validating the data ingested by the Data Ingestion component.
    It checks for the presence of required columns, data types, and performs statistical tests to ensure
    that the data meets the expected schema and quality standards.
    """
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact,
                 data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._scheme_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        """
        Reads data from the specified file path and returns it as a pandas DataFrame.
        """
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"The file {file_path} does not exist.")
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def validate_columns(self, dataframe: pd.DataFrame) -> bool:
        try:
            number_of_columns = len(self._scheme_config)
            logging.info(f"Required number of columns: {number_of_columns}.")
            logging.info(f"Dataframe has {len(dataframe.columns)} in total.")

            if (len(dataframe.columns == number_of_columns)):
               return True
            else:
                return False
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def validate_numerical_columns(self, dataframe: pd.DataFrame) -> bool:
        """
        Checks whether all required numerical columns (defined in the schema) exist in the dataframe
        and are of numeric type."""
        try:
            numerical_columns = self._scheme_config["numerical_columns"]
            dataframe_columns = dataframe.columns.tolist()
            
            for column in numerical_columns:
                if column not in dataframe_columns:
                    logging.error(f"Numerical column '{column}' is missing in the dataframe.")
                    return False
                if not np.issubdtype(dataframe[column].dtype, np.number):
                    logging.error(f"Column '{column}' is not numeric type.")
                    return False
            logging.info("All numerical columns are present and of numeric type.")
            return True
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def detect_dataset_drift(self, base_df, current_df, threshold = 0.05) -> bool:
        """
        If the file does not exist, it will create the necessary directories and write the file.
        Detects dataset drift by comparing the statistical distribution of the base dataset
        with the current dataset using the Kolmogorov-Smirnov test."""
        try:
            status = True
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_sample_dist = ks_2samp(d1, d2)
                p_value = is_sample_dist.pvalue
                if threshold <= p_value:
                    is_found = True
                else:
                    is_found = False
                    status = False
            
            report.update({column:{
                "p_value": float(p_value),
                "drift_status": is_found
            }})

            drift_report_file_path = self.data_validation_config.drift_report_file_path
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path, exist_ok = True)

            write_yaml_file(file_path = drift_report_file_path, content = report)

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def initiate_data_validation(self) -> DataIngestionArtifact:
        """
        Performs initial data validation by checking the presence of required columns
        and detecting data drift between the training and testing datasets.
        """
        try:
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            # Reading data from the train and test file path
            train_df = DataValidation.read_data(train_file_path)
            test_df = DataValidation.read_data(test_file_path)

            # Validating the number of columns
            status = self.validate_columns(dataframe = train_df)
            if not status:
                error_message = f"Training dataframe does not contain all columns!\n"
                raise(error_message)
            status = self.validate_columns(dataframe = test_df)
            if not status:
                error_message = f"Testing dataframe does not contain all columns!\n"
                raise(error_message)
            
            # Validating numerical columns
            status = self.validate_numerical_columns(train_df)
            if not status:
                raise Exception("Train data does not contain valid numerical columns.")

            status = self.validate_numerical_columns(test_df)
            if not status:
                raise Exception("Test data does not contain valid numerical columns.")

            # Checking data drift
            status = self.detect_dataset_drift(base_df = train_df, current_df = test_df)
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path, exist_ok =  True)

            # If no issue, save this as a csv file
            train_df.to_csv(self.data_validation_config.valid_train_file_path, index = False, header = True)
            test_df.to_csv(self.data_validation_config.valid_test_file_path, index = False, header = True)

            data_validation_artifact = DataValidationArtifact(
                validation_status = status,
                valid_train_file_path = self.data_ingestion_artifact.train_file_path,
                valid_test_file_path = self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path = None,
                invalid_test_file_path = None,
                drift_report_file_path = self.data_validation_config.drift_report_file_path
            )

            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)