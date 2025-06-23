import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer

from networksecurity.entity.config_entity import (
    TrainingPipelineConfig, DataIngestionConfig, DataValidationConfig, 
    DataTransformationConfig, ModelTrainerConfig
)

from networksecurity.entity.artifact_entity import (
    DataIngestionArtifact, DataValidationArtifact, 
    DataTransformationArtifact, ModelTrainerArtifact
)

from networksecurity.constants.training_pipeline import TRAINING_BUCKET_NAME
from networksecurity.cloud.s3_sync import S3Sync

class TrainingPipeline:
    """
    The TrainingPipeline class orchestrates the entire machine learning pipeline,
    from data ingestion to model training and artifact synchronization with AWS S3.
    It initializes the pipeline configuration, manages the sequence of operations,
    and handles exceptions that may arise during the process.
    """
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()
        self.s3_sync = S3Sync()
    
    def start_data_ingestion(self):
        try:
            self.data_ingestion_config = DataIngestionConfig(training_pipeline_config = self.training_pipeline_config)
            data_ingestion = DataIngestion(data_ingestion_config = self.data_ingestion_config)
            logging.info("Initializing Data Ingestion")
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            return data_ingestion_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact):
        try:
            data_validation_config = DataValidationConfig(training_pipeline_config = self.training_pipeline_config)
            data_validation = DataValidation(data_ingestion_artifact, data_validation_config)
            logging.info("Initializing Data Validation")
            data_validation_artifact = data_validation.initiate_data_validation()
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def start_data_transformation(self, data_validation_artifact: DataValidationArtifact):
        try:
            data_transformation_config = DataTransformationConfig(training_pipeline_config = self.training_pipeline_config)
            data_transformation = DataTransformation(data_validation_artifact, data_transformation_config)
            logging.info("Initializing Data Transformation")
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def start_model_training(self, data_transformation_artifact: DataTransformationArtifact) -> ModelTrainerArtifact:
        try:
            model_training_config = ModelTrainerConfig(training_pipeline_config = self.training_pipeline_config)
            model_training  = ModelTrainer(model_training_config, data_transformation_artifact)
            logging.info("Initializing Model Training")
            model_trainer_artifact = model_training.initiate_model_training() 
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    # Saving local artifact to the s3 bucket
    def sync_artifact_dir_to_s3(self):
        """
        The sync_artifact_dir_to_s3 method synchronizes the local artifact directory
        with an AWS S3 bucket. It constructs the S3 bucket URL using the training pipeline
        timestamp and uses the S3Sync class to perform the synchronization.
        """ 
        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/artifact/{self.training_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder = self.training_pipeline_config.artifact_dir, aws_bucket_url = aws_bucket_url)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    # Saving final models to the s3 bucket
    def sync_saved_model_dir_to_s3(self):
        """
        The sync_saved_model_dir_to_s3 method synchronizes the saved model directory
        with an AWS S3 bucket. It constructs the S3 bucket URL using the training pipeline
        timestamp and uses the S3Sync class to perform the synchronization.
        """
        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/finalmodels/{self.training_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder = self.training_pipeline_config.model_dir, aws_bucket_url = aws_bucket_url)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def run_pipeline(self):
        """
        The run_pipeline method orchestrates the entire training pipeline by sequentially
        executing the data ingestion, validation, transformation, and model training steps.
        It also handles synchronization of the artifact directory and saved model directory to AWS S3.
        """
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_validation_artifact)
            model_trainer_artifact = self.start_model_training(data_transformation_artifact)
            self.sync_artifact_dir_to_s3()
            self.sync_saved_model_dir_to_s3()
            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)