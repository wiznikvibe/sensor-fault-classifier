import os, sys
from src.logger import logging 
from src.exception import CustomException
from src.entity import config_entity, artifact_entity
from src.utils import write_yaml_file, convert_columns_float
from scipy.stats import ks_2samp
import pandas as pd 
import numpy as np
from typing import Optional


class DataValidation:

    def __init__(self, data_validation_config:config_entity.DataValidationConfig,
        data_ingestion_artifact:artifact_entity.DataIngestionArtifact):

        """
        Data Validation process generates a report summarizing the findings of comparision between base dataframe and 
        current dataframe. 
        """

        logging.info(f"{'*'*20}Data Validation Loading{'*'*20}")
        print(f"{'='*20}Data Validation Loading{'='*20}")
        self.data_validation_config = data_validation_config
        self.data_ingestion_artifact = data_ingestion_artifact
        self.validation_error = dict()

    
    def drop_missing_values_columns(self, df:pd.DataFrame, report_key: str)->Optional[pd.DataFrame]:
        '''
        Drop Columns With Missing Values Exceeding the Threshold parameter

        df: DataFrame Input Variable 
        threshold: Percentage Criteria to Drop Columns 
        returns Pandas DataFrame 
        '''
        try:
            threshold = self.data_validation_config.missing_values_threshold
            null_report = df.isnull().sum()/df.shape[0]
            logging.info(f"Selecting Columns with Missing values above {threshold} Threshold")
            drop_cols_list = null_report[null_report > threshold].index 

            self.validation_error[report_key] = list(drop_cols_list)
            df.drop(list(drop_cols_list), axis=1, inplace=True)

            if len(df.columns) == 0:
                logging.info("The Dataset has Missing values over threshold.")
                return None
            return df 
        except Exception as e:
            raise CustomException(e, sys) 

    
    def column_checker(self, base_df:pd.DataFrame, current_df:pd.DataFrame, report_key:str)->bool:
        """
        Compares the Base Dataframe with the Current DataFrame for Features and returns true/False.
        If all the features are present in Current DataFrame returns True, Else returns False.
        """
        try: 
            base_columns = base_df.columns 
            current_columns = current_df.columns 

            missing_columns = []
            for feature in base_columns:
                if feature not in current_columns:
                    logging.info(f'Column - {feature} Missing')
                    missing_columns.append(feature)

            if len(missing_columns) > 0:
                self.validation_error[report_key] = missing_columns
                return False 
            return True
        except Exception as e:
            raise CustomException(e, sys)

    
    def data_drift(self, base_df:pd.DataFrame, current_df:pd.DataFrame, report_key:str):
        """
        Data Drift occurs when the statistical properties of the model changes which results in poor performance 
        this can happen when the data used for the model building changes. This function returns the report regarding the Data Drift.
        """
        
        try: 
            drift_record = dict()

            base_columns = base_df.columns 
            current_columns = current_df.columns

            for feature in base_columns:
                base_data, current_data = base_df[feature], current_df[feature]
                logging.info(f"Running Kologomorov-Smirnov Test to Check If data belong to the same distribution")

                column_distribution = ks_2samp(base_data, current_data)

                if column_distribution.pvalue > 0.05:
                    drift_record[feature] = {
                        'is_same_distribution': True,
                        'p-value': float(column_distribution.pvalue)
                    } 
                else:
                    drift_record[feature] = {
                        'is_same_distribution': False,
                        'p-value': float(column_distribution.pvalue)
                    }
            
            self.validation_error[report_key] = drift_record
        except Exception as e:
            raise CustomException(e, sys)


    def initiate_data_validation(self,)-> artifact_entity.DataValidationArtifact:
        try:
            logging.info(f"Reading the Base Dataset, Treating for Missing Values")
            
            # Base DataFrame
            base_df = pd.read_csv(self.data_validation_config.base_file_dir)
            base_df.replace({'na':np.NAN}, inplace=True)
            base_df = self.drop_missing_values_columns(df=base_df, report_key="missing_data_baseframe")

            # Train and Test Split of the Data 
            train_df = pd.read_csv(self.data_ingestion_artifact.train_data_dir)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_data_dir)

            train_df = self.drop_missing_values_columns(df=train_df, report_key="missing_data_trainframe")
            test_df = self.drop_missing_values_columns(df=test_df, report_key="missing_data_testframe")
            
            exclude_column = [self.data_validation_config.target_column]
            base_df = convert_columns_float(df=base_df, exclude_columns=exclude_column)
            train_df = convert_columns_float(df=train_df, exclude_columns=exclude_column)
            test_df = convert_columns_float(df=test_df, exclude_columns=exclude_column)

            train_status = self.column_checker(base_df=base_df,current_df=train_df, report_key="missing_columns-train")
            test_status = self.column_checker(base_df=base_df,current_df=test_df, report_key="missing_columns-test")
            # print(train_status)
            # print(test_status)

            if train_status:
                self.data_drift(base_df=base_df, current_df=train_df, report_key="data_drift-train")

            if test_status:
                self.data_drift(base_df=base_df, current_df=test_df, report_key="data_drift-test")

            logging.info("Generating Validation Reports")
            write_yaml_file(file_path=self.data_validation_config.report_file_dir, data=self.validation_error)

            data_validation_artifact = artifact_entity.DataValidationArtifact(report_file_dir=self.data_validation_config.report_file_dir)
            logging.info(f"{'*'*20}Exiting Data Validation{'*'*20}")
            return data_validation_artifact
        except Exception as e:
            raise CustomException(e, sys)



