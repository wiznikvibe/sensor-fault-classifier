import os, sys
import pandas as pd 
import numpy as np 
from scipy.stats import ks_2samp
from imblearn.combine import SMOTETomek
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler
from sklearn.preprocessing import LabelEncoder
from src import utils
from src.exception import CustomException
from src.logger import logging 
from src.entity import config_entity, artifact_entity


class DataTransformation:

    def __init__(self, data_transformation_config:config_entity.DataTransformationConfig, data_ingestion_artifact:artifact_entity.DataIngestionArtifact):
        print(f"{'='*20}Data Transformation Loading{'='*20}")
        logging.info(f"{'='*20}Data Transformation Phase Initiated{'='*20}")
        self.data_transformation_config = data_transformation_config
        self.data_ingestion_artifact = data_ingestion_artifact


    @classmethod 
    def get_data_transformer_obj(cls)-> Pipeline:
        try:
            simple_imputer = SimpleImputer(strategy='mean', fill_value=0)
            robust_scaler = RobustScaler()

            pipeline = Pipeline(steps=[
                ("Imputer", simple_imputer),
                ('Scaler',robust_scaler)
            ]) 
            return pipeline

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_transformation(self,)-> artifact_entity.DataTransformationArtifact:
        try:
            train_df = pd.read_csv(self.data_ingestion_artifact.train_data_dir)
            test_df = pd.read_csv(self.data_ingestion_artifact.train_data_dir)

            input_train_df = train_df.drop(self.data_transformation_config.target_column, axis=1)
            input_test_df = test_df.drop(self.data_transformation_config.target_column, axis=1)

            target_train_df = train_df[self.data_transformation_config.target_column]
            target_test_df = test_df[self.data_transformation_config.target_column]

            # Label Encoding the Output Feature 
            logging.info("Applying the Label Encoder Transform over the Output Feature")
            label_encoder = LabelEncoder()
            label_encoder.fit(target_train_df)
            target_train_arr = label_encoder.transform(target_train_df)
            target_test_arr = label_encoder.transform(target_test_df)

            # Applying The Transformation Pipeline on the Input Features
            logging.info("Applying The Transformation Pipeline on the Input Features")
            transformation_pipeline = DataTransformation.get_data_transformer_obj()
            transformation_pipeline.fit(input_train_df)
            input_train_arr = transformation_pipeline.transform(input_train_df)
            input_test_arr = transformation_pipeline.transform(input_test_df)

            # Resampling Data for Minority Class Data 
            smt = SMOTETomek(sampling_strategy='minority', random_state=10)
            
            logging.info(f"Before resampling: Train Input Data: {input_train_arr.shape}, Target Data: {target_train_arr.shape}")
            input_train_feature_arr, target_train_arr = smt.fit_resample(input_train_arr,target_train_arr)
            logging.info(f"After resampling: Train Input Data: {input_train_feature_arr.shape}, Target Data: {target_train_arr.shape}")

            logging.info(f"Before resampling: Test Input Data: {input_test_arr.shape}, Target Data: {target_test_arr.shape}")
            input_test_feature_arr, target_test_arr = smt.fit_resample(input_test_arr,target_test_arr)
            logging.info(f"After resampling: Test Input Data: {input_test_feature_arr.shape}, Target Data: {target_test_arr.shape}")

            train_arr = np.c_[input_train_feature_arr, target_train_arr]
            test_arr = np.c_[input_test_feature_arr, target_test_arr]
            
            logging.info("Saving Transform Data into Numpy Object")
            utils.save_numpy_array_data(file_dir=self.data_transformation_config.transform_train_dir, array=train_arr)
            utils.save_numpy_array_data(file_dir=self.data_transformation_config.transform_test_dir, array=test_arr)

            utils.save_object(file_dir=self.data_transformation_config.transform_obj_dir, obj=transformation_pipeline)
            utils.save_object(file_dir=self.data_transformation_config.target_encoder_dir, obj=label_encoder)

            data_transformation_artifact = artifact_entity.DataTransformationArtifact(
                transform_obj_dir = self.data_transformation_config.transform_obj_dir,
                transform_train_dir = self.data_transformation_config.transform_train_dir,
                transform_test_dir = self.data_transformation_config.transform_test_dir,
                target_encoder_dir = self.data_transformation_config.target_encoder_dir
            )
            logging.info(f"{'='*20}Exiting Data Transformation Phase{'='*20}")
            return data_transformation_artifact
        
        except Exception as e: 
            raise CustomException(e, sys)