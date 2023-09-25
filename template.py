import os 
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)

project = 'src'

list_of_files = [
    f"{project}/__init__.py",
    f"{project}/logger.py",
    f"{project}/exception.py",
    f"{project}/config.py",
    f"{project}/utils.py",
    f"{project}/components/__init__.py",
    f"{project}/components/data_ingestion.py",
    f"{project}/components/data_transformation.py",
    f"{project}/components/data_validation.py",
    f"{project}/components/model_trainer.py",
    f"{project}/components/model_monitoring.py",
    f"{project}/components/model_pusher.py",
    f"{project}/entity/__init__.py",
    f"{project}/entity/config_entity.py",
    f"{project}/entity/artifact_entity.py",
    f"{project}/pipelines/__init__.py",
    f"{project}/pipelines/prediction_pipeline.py",
    f"{project}/pipelines/training_pipeline.py",
    "notebook/",
    "setup.py",
    "main.py"
]

for file in list_of_files:
    file_path = Path(file)
    file_dir, filename = os.path.split(file_path)

    if file_dir != "":
        os.makedirs(file_dir, exist_ok=True)
        logging.info(f"FILE STRUCTURE Implementation: {file_dir} for file-{filename}")
    
    if (not os.path.exists(file_path)) or (os.path.getsize(file_path)==0):
        with open(file_path, "w") as f:
            pass
        logging.info(f"Creating Empty Files: {file_path}")
    
    else:
        logging.info(f"Directory: {filename} already populated")