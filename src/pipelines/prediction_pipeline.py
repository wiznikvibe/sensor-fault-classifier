import os, sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd 
from src.predictor import ModelResolver
from src.utils import load_object
from datetime import datetime 
import numpy as np 

PREDICTION_DIR = "prediction"



def start_batch_prediction(input_file_path):
    try:
        logging.info("Batch Prediction Initiated")
        os.makedirs(PREDICTION_DIR, exist_ok=True)
        model_resolver = ModelResolver(model_registry="saved_models")
        
        logging.info(f"Reading File : {input_file_path}") 
        df = pd.read_csv(input_file_path)
        df.replace({"na": np.NAN}, inplace=True)
        
        logging.info(f"Loading Transformer to Transform dataset")
        transformer = load_object(model_resolver.get_latest_transformer_path())
        input_features_name =   list(transformer.feature_names_in_)
        input_arr = transformer.transform(df[input_features_name])

        logging.info(f"Loading Model to make prediction dataset")
        model = load_object(model_resolver.get_latest_model_path())

        prediction = model.predict(input_arr)

        logging.info("Decoding the Predictions down to Their Categories")
        target_encoder = load_object(model_resolver.get_latest_target_encoder_path())
        cat_prediction = target_encoder.inverse_transform(prediction)

        df['prediction'] = prediction
        df['cat_pred'] = cat_prediction
        
        prediction_file_name = os.path.basename(input_file_path).replace(".csv",f"{datetime.now().strftime('%m%d%Y__%H%M%S')}.csv")
        prediction_file_path = os.path.join(PREDICTION_DIR,prediction_file_name)
        df.to_csv(prediction_file_path, index=False, header=True)
        return prediction_file_path
    except Exception as e:
        raise CustomException(e, sys)