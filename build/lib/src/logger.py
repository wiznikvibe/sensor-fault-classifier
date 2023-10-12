from datetime import datetime 
import logging
import os

# Log File Name 
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%m_%S')}.log"

# File Directory  
log_path = os.path.join(os.getcwd(),"logs", LOG_FILE)
os.makedirs(log_path, exist_ok=True)

# Log File inside in Directory for the Log folder
LOG_FILE_PATH = os.path.join(log_path, LOG_FILE)

# Configuration Setting 
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format= "[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)