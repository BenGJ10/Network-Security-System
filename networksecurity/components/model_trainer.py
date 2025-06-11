import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.entity.artifact_entity import (
    DataTransformationArtifact,
    ModelTrainerArtifact)

from networksecurity.utils.main_utils.utils import load_object, save_object, save_numpy_array_data, load_numpy_array_data
from networksecurity.utils.main_utils.utils import evaluate_models
from networksecurity.utils.ml_utils.metric.classification_metrics import get_classification_score
from networksecurity.utils.ml_utils.model.estimator import NetworkModel

# ML Algorithms for model training
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier, GradientBoostingClassifier, RandomForestClassifier
import mlflow

class ModelTrainer:
    def __init__(self, model_trainer_config: ModelTrainerConfig, data_transformation_artifact: DataTransformationArtifact):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def track_mlflow(self, best_model, classification_metric):
        with mlflow.start_run():
            f1_score = classification_metric.f1_score
            precision_score = classification_metric.precision_score
            recall_score = classification_metric.recall_score

            mlflow.log_metric("f1_score", f1_score)
            mlflow.log_metric("precision", precision_score)
            mlflow.log_metric("recall_score", recall_score)

    
    def train_model(self, x_train, y_train, x_test, y_test):
        models = {
            "Random Forest": RandomForestClassifier(),
            "Decision Tree": DecisionTreeClassifier(),
            "Gradient Boosting": GradientBoostingClassifier(), # use verbose = 1 for seeing the model training
            "AdaBoost": AdaBoostClassifier(),
            "Logistic Regression": LogisticRegression(),
        }

        params = {
            "Decision Tree": {
                'criterion':['gini', 'entropy', 'log_loss'],
                # 'splitter':['best','random'],
                # 'max_features':['sqrt','log2'],
            },
            "Random Forest":{
                # 'criterion':['gini', 'entropy', 'log_loss'],
                # 'max_features':['sqrt','log2',None],
                'n_estimators': [8,16,32,128,256]
            },
            "Gradient Boosting":{
                # 'loss':['log_loss', 'exponential'],
                'learning_rate':[.1,.01,.05,.001],
                'subsample':[0.6,0.7,0.75,0.85,0.9],
                # 'criterion':['squared_error', 'friedman_mse'],
                # 'max_features':['sqrt','log2'],
                'n_estimators': [8,16,32,64,128,256]
            },
            "Logistic Regression":{},
            "AdaBoost":{
                'learning_rate':[.1,.01,.001],
                'n_estimators': [8,16,32,64,128,256]
            }            
        }

        model_report: dict = evaluate_models(x_train, y_train, x_test, y_test, models, params)

        # To get the best model score from the model report
        best_model_score = max(sorted(model_report.values()))

        # To get the best mode name from the model report
        best_model_name = list(model_report.keys())[
            list(model_report.values()).index(best_model_score)
        ]
        logging.info(f"Best model selected: {best_model_name} with score: {best_model_score}")
        
        best_model = models[best_model_name]
        
        best_model.fit(x_train, y_train)

        # Training the best model
        y_train_pred = best_model.predict(x_train)
        classification_train_metric = get_classification_score(y_train, y_train_pred)
        
        # Tracking the MLFLOW
        self.track_mlflow(best_model, classification_train_metric)

        # Predicting the test data with the best model
        y_test_pred = best_model.predict(x_test)
        classification_test_metric = get_classification_score(y_test, y_test_pred)

        # Saving the model 
        preprocessor = load_object(self.data_transformation_artifact.transformed_object_file_path)
        model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(model_dir_path, exist_ok = True)

        network_model = NetworkModel(preprocessor, best_model)
        save_object(self.model_trainer_config.trained_model_file_path, network_model)

        # Model Trainer Artifact
        model_trainer_artifact =  ModelTrainerArtifact(trained_model_file_path = self.model_trainer_config.trained_model_file_path,
                            train_metric_artifact = classification_train_metric,
                            test_metric_artifact = classification_test_metric,
                            )
        
        logging.info(f"Model trainer artifact: {model_trainer_artifact}")
        return model_trainer_artifact



    def initiate_model_training(self) -> ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            # Loading training and testing array
            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)

            x_train, y_train = train_arr[:, :-1], train_arr[:, -1]
            x_test, y_test = test_arr[:, :-1], test_arr[:, -1]

            model_trainer_artifact = self.train_model(x_train, y_train, x_test, y_test)
            return model_trainer_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
