from src.db_conn import mongo_client
from src.logger import logging
from src.exception import CustomException
import pandas as pd
import os, sys
import yaml, dill 


def get_collection_dataframe(database_name:str, collection_name:str)->pd.DataFrame:
    """
    This function returns Collection from the database as dataframe
    """
    try: 
        logging.info(f"Reading Data From DataBase: {database_name}, accessing Collection: {collection_name}")
        df = pd.DataFrame(list(mongo_client[database_name][collection_name].find()))
        logging.info(f"Shape of the Dataset: {df.shape}")
        if "_id" in df.columns:
            df.drop("_id", axis=1, inplace=True)
        
        return df 
        
        # print(df.head())
    except Exception as e:
        raise CustomException(e, sys)

def write_yaml_file(file_path, data:dict):
    try: 
        file_dir = os.path.dirname(file_path)
        os.makedirs(file_dir, exist_ok=True)
        with open(file_path, "w") as file_obj:
            yaml.dump(data, file_obj)

            file_obj.close()

    except Exception as e:
        raise CustomException(e, sys)

