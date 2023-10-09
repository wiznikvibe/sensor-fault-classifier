import os 
import sys 
from src.logger import logging
from src.exception import CustomException
from src.entity import config_entity, artifact_entity
from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation 
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.components.model_monitoring import ModelEvaluation
from src.components.model_pusher import ModelPusher

if __name__ == "__main__":
    try:
        training_pipeline_config = config_entity.TrainingPipelineConfig()
        data_ingestion_config = config_entity.DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        
        data_validation_config = config_entity.DataValidationConfig(training_pipeline_config=training_pipeline_config)
        data_validation = DataValidation(data_validation_config=data_validation_config,data_ingestion_artifact=data_ingestion_artifact)
        data_validation_artifacts = data_validation.initiate_data_validation()
        # print(data_validation_artifacts) 

        data_transformation_config = config_entity.DataTransformationConfig(training_pipeline_config=training_pipeline_config)
        data_transformation = DataTransformation(data_transformation_config=data_transformation_config, data_ingestion_artifact=data_ingestion_artifact)
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        # print(data_transformation_artifact)

        model_trainer_config = config_entity.ModelTrainerConfig(training_pipeline_config=training_pipeline_config)
        model_trainer = ModelTrainer(model_trainer_config=model_trainer_config, data_transformation_artifact=data_transformation_artifact)
        model_trainer_artifact = model_trainer.initiate_model_trainer()
        # print(model_trainer_artifact)

        # Model Evaluation 
        model_eval_config = config_entity.ModelEvaluationConfig(training_pipeline_config=training_pipeline_config)
        model_eval = ModelEvaluation(model_eval_config=model_eval_config,data_ingestion_artifact=data_ingestion_artifact,data_transformation_artifact=data_transformation_artifact,model_trainer_artifact=model_trainer_artifact)
        model_eval_artifact = model_eval.initiate_model_evaluation()
        
        # Model Pusher 
        model_pusher_config = config_entity.ModelPusherConfig(training_pipeline_config=training_pipeline_config)
        model_pusher = ModelPusher(model_pusher_config=model_pusher_config, data_transformation_artifact=data_transformation_artifact,model_trainer_artifact=model_trainer_artifact)
        model_pusher_artifact = model_pusher.initiate_model_pusher()
        print(model_pusher_artifact)
    except Exception as e:
        logging.info(e)
        # logging.info("Logging and Custom Exceptions Practical Execution")
        raise CustomException(e,sys)