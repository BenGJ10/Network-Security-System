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