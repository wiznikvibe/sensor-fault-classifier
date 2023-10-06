import os 
import sys 
from src.logger import logging
from src.exception import CustomException
from src.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig, DataValidationConfig
from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation 

if __name__ == "__main__":
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        data_ingestion_artifacts = data_ingestion.initiate_data_ingestion()
        
        data_validation_config = DataValidationConfig(training_pipeline_config=training_pipeline_config)
        data_validation = DataValidation(data_validation_config=data_validation_config,data_ingestion_artifact=data_ingestion_artifacts)
        data_validation_artifacts = data_validation.initiate_data_validation()
        print(data_validation_artifacts) 
         
    except Exception as e:
        logging.info(e)
        # logging.info("Logging and Custom Exceptions Practical Execution")
        raise CustomException(e,sys)