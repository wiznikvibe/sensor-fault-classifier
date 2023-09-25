import os, sys 
from datetime import datetime 
from src.logger import logging
from src.exception import CustomException

FILE_NAME = "raw.csv"
TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"

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
            self.train_data_dir = os.path.join(self.data_ingestion_dir,"raw_data", TRAIN_FILE_NAME)
            self.test_data_dir = os.path.join(self.data_ingestion_dir,"raw_data", TEST_FILE_NAME)
            self.test_size = 0.2
        except Exception as e: 
            raise CustomException(e, sys)

