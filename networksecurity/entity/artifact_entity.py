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

@dataclass
class DataTransformationArtifact:
    """
    Data class for storing paths related to data transformation artifacts.
    This class holds the file paths for transformed object files and transformed training and testing datasets.
    """
    transformed_object_file_path: str   
    transformed_train_file_path: str
    transformed_test_file_path: str

@dataclass
class ClassificationMetricArtifact:
    """
    Data class for storing classification metrics.
    This class holds the F1 score, precision, and recall score for a classification model.
    """
    f1_score: float
    precision: float
    recall_score: float
    
@dataclass
class ModelTrainerArtifact:
    """
    Data class for storing model training artifacts.
    This class holds the path to the trained model file and the metric artifacts for both training and testing datasets.
    """
    trained_model_file_path: str
    train_metric_artifact: ClassificationMetricArtifact
    test_metric_artifact: ClassificationMetricArtifact