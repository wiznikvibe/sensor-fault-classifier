from src.predictor import ModelResolver
from src.entity import config_entity, artifact_entity
from src.exception import CustomException
from src.logger import logging
from src.utils import load_object

from sklearn.metrics import f1_score
import os, sys
import pandas as pd 


class ModelEvaluation:
    
    def __init__(self, 
        model_eval_config:config_entity.ModelEvaluationConfig,
        data_ingestion_artifact:artifact_entity.DataIngestionArtifact,
        data_transformation_artifact: artifact_entity.DataTransformationArtifact,
        model_trainer_artifact: artifact_entity.ModelTrainerArtifact
        ):
        print(f"{'='*20}Model Evaluation{'='*20}")
        self.model_eval_config = model_eval_config
        self.data_ingestion_artifact = data_ingestion_artifact
        self.data_transformation_artifact = data_transformation_artifact
        self.model_trainer_artifact = model_trainer_artifact
        self.model_resolver = ModelResolver()


    def initiate_model_evaluation(self)-> artifact_entity.ModelEvaluationArtifact:
        try:
            logging.info("Evaluation Inititated")
            latest_dir_path = self.model_resolver.get_latest_dir_path()
            if latest_dir_path == None:
                model_eval_artifact = artifact_entity.ModelEvaluationArtifact(is_model_accepted=True,
                improved_accuracy=None)
                logging.info(f"Model Evaluation Carried Out findings: {model_eval_artifact}")
                return model_eval_artifact
            
            logging.info("Finding Location for Model, Target Encoder and Transformer") 
            transformer_path = self.model_resolver.get_latest_transformer_path()
            model_path = self.model_resolver.get_latest_model_path()
            target_enc_path = self.model_resolver.get_latest_target_encoder_path()
            
            logging.info("Loading Previous trained objects")
            transformer = load_object(file_dir=transformer_path)
            model = load_object(file_dir=model_path)
            target_encoder = load_object(file_dir=target_enc_path)

            logging.info("Loading Currently trained objects") 
            current_transformer = load_object(file_dir=self.data_transformation_artifact.transform_obj_dir)
            current_model = load_object(file_dir=self.model_trainer_artifact.model_path)
            current_target_enc = load_object(file_dir=self.data_transformation_artifact.target_encoder_dir)

            test_df = pd.read_csv(self.data_ingestion_artifact.test_data_dir)
            target_df = test_df[self.model_eval_config.target_column]
            y_true = target_encoder.transform(target_df)

            logging.info("Accuracy Using Previously trained model")
            input_features_name = list(transformer.feature_names_in_)
            input_arr = transformer.transform(test_df[input_features_name])
            y_pred = model.predict(input_arr)
            print(f"Prediction using previous model: {target_encoder.inverse_transform(y_pred[:5])}")
            previous_model_score = f1_score(y_true=y_true, y_pred=y_pred)
            logging.info(f"Accuracy using previous trained model: {previous_model_score}")


             
            input_features_name = list(current_transformer.feature_names_in_)
            input_arr = current_transformer.transform(test_df[input_features_name])
            y_pred = current_model.predict(input_arr)
            y_true = current_target_enc.transform(target_df)

            current_model_score = f1_score(y_true=y_true, y_pred=y_pred)
            logging.info(f"Accuracy using current trained model: {current_model_score}")
            if current_model_score<=previous_model_score:
                logging.info(f"Current trained model is not better than previous model")
                raise Exception("Current trained model is not better than previous model")

            model_eval_artifact = artifact_entity.ModelEvaluationArtifact(is_model_accepted=True,
            improved_accuracy=current_model_score-previous_model_score)
            logging.info(f"Model eval artifact: {model_eval_artifact}")
            return model_eval_artifact

            # print(target_encoder.inverse_transform(prediction[:5]))
            # previous_model_score = f1_score(y_true=y_true,y_pred=y_pred)

            # logging.info("Accuracy Using Currently Trained Model")
            # input_arr = current_transformer.transform(test_df)
            # current_y_true = current_target_enc.transform(target_df)
            # current_y_pred = current_model.predict(input_arr)
            # print(current_target_enc.inverse_transform(prediction[:5]))
            # current_model_score = f1_score(y_true=current_y_true,y_pred=current_y_pred)


            # if current_model_score < previous_model_score:
            #     raise Exception("Current Trained model is not better than the previous model")
            
            # model_eval_artifact = artifact_entity.ModelEvaluationArtifact(is_model_accepted=True,
            # improved_accuracy=current_model_score - previous_model_score)

            # logging.info(f"Improved Accuracy: {improved_accuracy} %")
            # return model_eval_artifact

        except Exception as e: 
            raise CustomException(e, sys)    
