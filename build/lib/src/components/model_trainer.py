import os, sys 
import numpy as np
import pandas as pd 
from xgboost import XGBClassifier
from sklearn.metrics import f1_score
from src import utils
from src.exception import CustomException
from src.logger import logging 
from src.entity import config_entity, artifact_entity

class ModelTrainer:

    def __init__(self, model_trainer_config:config_entity.ModelTrainerConfig, data_transformation_artifact:artifact_entity.DataTransformationArtifact):
        print(f"{'='*20}Model Trainer{'='*20}")
        logging.info(f"{'=='*20}Model Trainer Phase{'=='*20}")
        self.model_trainer_config = model_trainer_config
        self.data_transformation_artifact = data_transformation_artifact

    def train_model(self, x, y):
        try:
            clf = XGBClassifier()
            clf.fit(x,y)
            return clf   
        except Exception as e: 
            raise CustomException(e, sys)

    def initiate_model_trainer(self)-> artifact_entity.ModelTrainerArtifact:
        try:
            logging.info(f"Loading Transformed Train Directory: {self.data_transformation_artifact.transform_train_dir} || Transformer Test Directory: {self.data_transformation_artifact.transform_test_dir}")
            train_df = utils.load_numpy_arr_data(file_dir=self.data_transformation_artifact.transform_train_dir)
            test_df = utils.load_numpy_arr_data(file_dir=self.data_transformation_artifact.transform_test_dir) 
            
            logging.info("Splitting the dataset into Dependent and Independent Feature DataFrames")
            X_train, y_train = train_df[:,:-1], train_df[:,-1]
            X_test, y_test = test_df[:,:-1], test_df[:,-1]

            logging.info("Training the Model using the Train Transformed Data, Evaluating Model Performance")
            model = self.train_model(x=X_train,y=y_train)
            y_train_pred = model.predict(X_train)
            f1_train_score = f1_score(y_true=y_train, y_pred=y_train_pred)

            y_test_pred = model.predict(X_test)
            f1_test_score = f1_score(y_true=y_test, y_pred=y_test_pred) 

            logging.info(f"Comparing The Model Score against Expected Score: {self.model_trainer_config.expected_score}")
            logging.info("Checking for Underfitting and Overfitting Condition.")
            if f1_test_score < self.model_trainer_config.expected_score:
                raise Exception(f"Model is not good; As it is unable to generate Accuracy: {self.model_trainer_config.expected_score} ")
            
            diff = abs(f1_train_score - f1_test_score)
            if diff > self.model_trainer_config.overfitting_thres:
                raise Exception(f"Difference of Train/Test Score {diff} > {self.model_trainer_config.overfitting_thres}")

            utils.save_object(file_dir=self.model_trainer_config.model_path, obj=model) 
            model_trainer_artifact = artifact_entity.ModelTrainerArtifact(
                model_path=self.model_trainer_config.model_path,
                f1_train_score=f1_train_score,
                f1_test_score=f1_test_score
            )
            logging.info(f"{'=='*20}Exiting Model Trainer Phase{'=='*20}")
            return model_trainer_artifact

        except Exception as e:
            raise CustomException(e, sys)
