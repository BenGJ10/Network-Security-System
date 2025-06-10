import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer

if __name__ == "__main__":
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        logging.info("Initiating Data ingestion..")
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info("Data ingestion successfully completed.")
        print(data_ingestion_artifact)

        data_validation_config = DataValidationConfig(training_pipeline_config)
        data_validation = DataValidation(data_ingestion_artifact, data_validation_config)
        logging.info("Initiating Data validation..")
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info("Data validation successfully completed.")
        print(data_validation_artifact)

        data_transformation_config = DataTransformationConfig(training_pipeline_config)
        data_transformation = DataTransformation(data_validation_artifact, data_transformation_config) 
        logging.info("Initiating Data transformation..")
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        logging.info("Data transformation successfully completed.")
        print(data_transformation_artifact)


        model_trainer_config = ModelTrainerConfig(training_pipeline_config)
        model_trainer = ModelTrainer(model_trainer_config, data_transformation_artifact)
        logging.info("Initiating Model Training..")
        model_trainer_artifact = model_trainer.initiate_model_training()
        logging.info("Model training successfully completed.")
        print(model_trainer_artifact)

    except Exception as e:
            raise NetworkSecurityException(e, sys)