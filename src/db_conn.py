import os, sys
import pymongo
from dataclasses import dataclass 



@dataclass
class EnviromentVariables:
    """
    Enviroment Variables help keep the 
    data encryption and not reveal important credentials
    """
    mongodb_url:str = os.getenv("MONGO_DB_URL")

env_vars = EnviromentVariables()
mongo_client = pymongo.MongoClient(env_vars.mongodb_url)

TARGET_COLUMN = "class"