import os, sys 
import pandas as pd 
from predictor import ModelResolver
from src.utils import load_object
from src.exception import CustomException
from src.logger import logging 
from sklearn.metrics import f1_score
from src.entity import config_entity, artifact_entity

class ModelEvaluation:

    def __init__(
        self,
        model_eval_config: config_entity.ModelEvaluationConfig,
        data_ingestion_artifact: artifact_entity.DataIngestionArtifact,
        data_transformation_artifact: artifact_entity.DataTransformationArtifact,
        model_trainer_artifact: artifact_entity.ModelTrainerArtifact
    ):

        print(f"{'='*20}Data Evaluation{'='*20}")
        self.model_eval_config = model_eval_config
        self.data_ingestion_artifact = data_ingestion_artifact
        self.data_transformation_artifact = data_transformation_artifact
        self.model_trainer_artifact = model_trainer_artifact
        self.model_resolver = ModelResolver()

    
    def initiate_model_evaluation(self,)-> artifact_entity.ModelEvaluationArtifact:
        try: 
            logging.info(f"{'='*20}Data Evaluation{'='*20}")
            latest_dir_path = self.model_resolver.get_latest_dir_path()
            if latest_dir_path == None:
                model_eval_artifact = artifact_entity.ModelEvaluationArtifact(
                    is_model_accepted=True,
                    improved_accuracy=None
                )
                return model_eval_artifact
            
            logging.info("Searching directory path for - Transformer, Model, Encoder")
            transformer_path = self.model_resolver.get_latest_transformer_path()
            model_path = self.model_resolver.get_latest_model_path()
            target_enc_path = self.model_resolver.get_latest_target_encoder_path()

            logging.info("Loading the trained Objects")
            transformer = load_object(file_dir=transformer_path)
            model = load_object(file_dir=model_path)
            target_enc = load_object(file_dir=target_enc_path)

            logging.info("Loading objects to be trained.")
            current_transformer = load_object(file_dir=self.data_transformation_artifact.transform_obj_dir)
            current_model = load_object(file_dir=self.model_trainer_artifact.model_path)
            current_target_enc = load_object(file_dir=self.data_transformation_artifact.target_encoder_dir)
            
            test_df = pd.read_csv(self.data_ingestion_artifact.test_data_dir)
            target_df = test_df[self.model_eval_config.target_column]
            y_true = target_enc.transform(target_df)

            # logging.info("Accuracy for trained model")
            input_features = list(transformer.feature_names_in_)
            input_df = transformer.transform(test_df[input_features])
            y_pred = model.predict(input_df)
            trained_model_score = f1_score(y_true=y_true,y_pred=y_pred)
            logging.info(f"Accuracy for Trained Model: {trained_model_score}")

            input_features_name = list(current_transformer.feature_names_in_)
            input_df = current_transformer.transform(test_df[input_features_name])
            y_pred = current_model.predict(input_df)
            y_true = current_target_enc.transform(target_df)

            current_model_score = f1_score(y_pred=y_pred,y_true=y_true)
            logging.info(f"Accuracy for Current Trained Model: {current_model_score}")
            if current_model_score <= trained_model_score:
                logging.info(f"Model in production is better than model being trained")
                raise Exception(f"Model in production is better than model being trained")
            model_eval_artifact = artifact_entity.ModelEvaluationArtifact(
                is_model_accepted = True,
                improved_accuracy= current_model_score - trained_model_score
            )
            logging.info(f"{'='*20} Exiting Model Evaluation Phase {'='*20}")
            return model_eval_artifact
        except Exception as e: 
            raise CustomException(e, sys)
