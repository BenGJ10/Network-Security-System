from datetime import datetime
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from networksecurity.constants import training_pipeline
print(training_pipeline.DATA_INGESTION_DATABASE_NAME)


class TrainingPipelineConfig:
    """
    Sets up high-level configurations such as naming the pipeline and creating a timestamped artifact
    directory to store outputs
    """
    def __init__(self, timestamp = datetime.now()):
        timestamp = timestamp.strftime("%Y-%m-%d-%H-%M-%S")
        self.pipeline_name = training_pipeline.PIPELINE_NAME
        self.artifact_name = training_pipeline.ARTIFCAT_DIR
        self.artifact_dir = os.path.join(self.artifact_name, timestamp)
        self.timestamp = timestamp

class DataIngestionConfig:
    """
    Configuration class for the data ingestion component of the pipeline.

    This includes:
    - Where to store raw and split data.
    - File paths for training/testing data.
    - Settings like train/test split ratio.
    - The MongoDB collection and database names from constants.
    """
    def __init__(self, training_pipeline_config: TrainingPipelineConfig):
        self.data_ingestion_dir: str = os.path.join(
            training_pipeline_config.artifact_dir, training_pipeline.DATA_INGESTION_DIR_NAME
        )

        # File path where the full dataset (feature store) will be saved
        self.feature_store_file_path: str = os.path.join(
            self.data_ingestion_dir, training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR, training_pipeline.FILE_NAME
        )

        # Paths for the training and testing datasets after the split
        self.training_file_path: str = os.path.join(    
            self.data_ingestion_dir, training_pipeline.DATA_INGESTION_INGESTED_DIR, training_pipeline.TRAIN_FILE_NAME
        )

        self.testing_file_path: str = os.path.join(
            self.data_ingestion_dir, training_pipeline.DATA_INGESTION_INGESTED_DIR, training_pipeline.TEST_FILE_NAME    
        )

        self.train_test_split_ratio: float = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        
        # MongoDB configurations
        self.collection_name: str = training_pipeline.DATA_INGESTION_COLLECTION_NAME
        self.database_name: str = training_pipeline.DATA_INGESTION_DATABASE_NAME
