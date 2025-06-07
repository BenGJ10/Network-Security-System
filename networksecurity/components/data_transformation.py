import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from networksecurity.constants.training_pipeline import TARGET_COLUMN
from networksecurity.constants.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.entity.artifact_entity import (
    DataTransformationArtifact,
    DataValidationArtifact)
from networksecurity.utils.main_utils.utils import save_numpy_array, save_object