import os, sys
from src import utils
from src.entity import config_entity
from src.entity import artifact_entity
from src.exception import CustomException
from sklearn.model_selection import train_test_split
from src.logger import logging
import pandas as pd 
import numpy as np 


class DataIngestion:

    def __init__(self,data_ingestion_config: config_entity.DataIngestionConfig):
        try:
            logging.info(f"{'*'*20}Data Ingestion Loading{'*'*20}")
            print(f"{'*'*20}Data Ingestion Loading{'*'*20}")
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise CustomException(e,sys)
         
    
    def initiate_data_ingestion(self)->artifact_entity.DataIngestionArtifact:
        try:
            # logging.info(f"{'='*20}Data Ingestion{'='*20}")
            # print(f"{'='*20}Data Ingestion{'='*20}")
            logging.info("Initiate Data Ingestion, Exporting Data as a Dataframe...")
            df:pd.DataFrame = utils.get_collection_dataframe(
                database_name=self.data_ingestion_config.database_name,
                collection_name=self.data_ingestion_config.collection_name
            )
            # print(type(df))
            df.replace(to_replace="na",value=np.NAN,inplace=True)

            logging.info("Save Data into Raw Data")
            raw_data_path = os.path.dirname(self.data_ingestion_config.raw_data_dir)
            os.makedirs(raw_data_path, exist_ok=True)
            logging.info("Raw Data Directory Initialised")
            df.to_csv(path_or_buf=self.data_ingestion_config.raw_data_dir, index=False, header=True)


            logging.info(">>>Data Segregation Process Initiated<<<")
            train_df, test_df = train_test_split(df,test_size=self.data_ingestion_config.test_size,random_state=42)

            dataset_dir = os.path.dirname(self.data_ingestion_config.train_data_dir)
            os.makedirs(dataset_dir, exist_ok=True)

            logging.info("Save Training and Testing Datasets")
            train_df.to_csv(path_or_buf=self.data_ingestion_config.train_data_dir, index=False, header=True)
            test_df.to_csv(path_or_buf=self.data_ingestion_config.test_data_dir, index=False, header=True)
            
            # Artifact Initializer
            data_ingestion_artifacts = artifact_entity.DataIngestionArtifact(
                raw_data_dir=self.data_ingestion_config.raw_data_dir,
                train_data_dir=self.data_ingestion_config.train_data_dir,
                test_data_dir=self.data_ingestion_config.test_data_dir
            )

            logging.info(f"Data Ingestion artifact: {data_ingestion_artifacts}")
            logging.info(f"{'*'*20}Exiting Data Ingestion Phase{'*'*20}")
            return data_ingestion_artifacts


        except Exception as e:
            logging.info(e,sys)
            raise CustomException(e,sys)