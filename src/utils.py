from src.db_conn import mongo_client
from src.logger import logging
from src.exception import CustomException
import pandas as pd
import numpy as np
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


def save_object(file_dir: str, obj: object)->None:
    try: 
        logging.info("Entered the save object method of Utils Class")
        os.makedirs(os.path.dirname(file_dir), exist_ok=True)
        with open(file_dir, "wb") as file_obj:
            dill.dump(obj, file_obj)
        logging.info("Exited the model saving method of Utils Class ")
    except Exception as e:
        raise CustomException(e, sys)


def save_numpy_array_data(file_dir: str, array: np.array):
    try:
        
        os.makedirs(os.path.dirname(file_dir), exist_ok=True)
        with open(file_dir, "wb") as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise CustomException(e, sys)


def load_object(file_dir:str,)->object:
    try:
        if not os.path.exists(file_dir):
            logging.info(Exception(f"The: {file_dir} does not exist"))
        with open(file_dir, "rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise CustomException(e, sys)


def load_numpy_arr_data(file_dir:str) -> np.array:
    try:
        with open(file_dir, "rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise CustomException(e, sys)

