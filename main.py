import os,sys
from src.pipelines.training_pipeline import start_training_pipeline
from src.logger import logging
from src.exception import CustomException
from src.pipelines.prediction_pipeline import start_batch_prediction 

file_path = "C:/Users/nikhi/sensor-fault-classifier/aps_failure_training_set1.csv"

if __name__ == "__main__":
    try:
        output = start_batch_prediction(input_file_path=file_path)
        print(output)
    except Exception as e:
        logging.info(e)
        # logging.info("Logging and Custom Exceptions Practical Execution")
        raise CustomException(e,sys)