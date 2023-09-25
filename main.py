import os 
import sys 
from src.utils import get_collection_dataframe
from src.logger import logging
from src.exception import CustomException
from src.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig


if __name__ == "__main__":
    try:
        training_pipeline_config = TrainingPipelineConfig()
        data_ingstion_config = DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        get_collection_dataframe(database_name=data_ingstion_config.database_name,collection_name=data_ingstion_config.collection_name)
         
    except Exception as e:
        logging.info(e)
        # logging.info("Logging and Custom Exceptions Practical Execution")
        raise CustomException(e,sys)