from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    """
    Data class for storing paths related to data ingestion artifacts.
    This class holds the file paths for training and testing datasets
    after they have been processed and split from the original dataset.    
    """
    train_file_path: str
    test_file_path: str

@dataclass
class DataValidationArtifact:
    """
    Data class for storing paths related to data validation artifacts.
    This class holds the file paths for valid and invalid training and testing datasets,
    as well as the path for the drift report file.
    """
    validation_status: bool
    valid_train_file_path: str
    valid_test_file_path: str
    invalid_train_file_path: str
    invalid_test_file_path: str
    drift_report_file_path: str