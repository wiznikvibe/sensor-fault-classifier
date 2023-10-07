import os, sys 
from datetime import datetime 
from src.logger import logging
from src.exception import CustomException

FILE_NAME = "raw_data.csv"
TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"
TRANSFORMER_OBJ_FILE_NAME = "transformer.pkl"
TARGET_ENCODER_OBJ_FILE_NAME = "target_encoder.pkl"
MODEL_FILE_NAME = 'model.pkl'

class TrainingPipelineConfig:
    """
    Artifact Directory Creation which is Output Configuration Folder for the 
    project.
    """
    def __init__(self):
        try:
            self.artifact_dir = os.path.join(os.getcwd(), "artifact", f"{datetime.now().strftime('%m%d%Y_%H%M%S')}")
        except Exception as e:
            raise CustomException(e, sys)

class DataIngestionConfig:
    """ Setting the Input Variable Configuration for Data Ingestion """

    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        try:
            self.database_name = 'aps'
            self.collection_name = 'sensor'
            self.data_ingestion_dir = os.path.join(training_pipeline_config.artifact_dir, "data_ingestion")
            self.raw_data_dir = os.path.join(self.data_ingestion_dir,"raw_data", FILE_NAME)
            self.train_data_dir = os.path.join(self.data_ingestion_dir,"dataset", TRAIN_FILE_NAME)
            self.test_data_dir = os.path.join(self.data_ingestion_dir,"dataset", TEST_FILE_NAME)
            self.test_size = 0.2
        except Exception as e: 
            raise CustomException(e, sys)

    def to_dict(self,)->dict:
        try:
            return self.__dict__
        except Exception as e:
            raise CustomException(e, sys)


class DataValidationConfig:

    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        self.data_validation_dir = os.path.join(training_pipeline_config.artifact_dir, "data_validation")
        self.report_file_dir = os.path.join(self.data_validation_dir, "report.yaml")
        self.missing_values_threshold: float = 0.2
        self.base_file_dir = os.path.join("aps_failure_training_set1.csv")

    
class DataTransformationConfig:
    def __init__(self, training_pipeline_config:TrainingPipelineConfig):
        self.target_column = "class"
        self.data_transformation_dir = os.path.join(training_pipeline_config.artifact_dir,"data_transformation")
        self.transform_obj_dir = os.path.join(self.data_transformation_dir,'transformer', TRANSFORMER_OBJ_FILE_NAME)
        self.transform_train_dir = os.path.join(self.data_transformation_dir,'transformer',TRAIN_FILE_NAME.replace('csv','npz'))
        self.transform_test_dir = os.path.join(self.data_transformation_dir,'transformer',TEST_FILE_NAME.replace('csv','npz'))
        self.target_encoder_dir = os.path.join(self.data_transformation_dir,'transformer',TARGET_ENCODER_OBJ_FILE_NAME)


class ModelTrainerConfig:...

class ModelEvaluationConfig:...

class ModelPusherConfig:...