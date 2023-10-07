from dataclasses import dataclass 

@dataclass
class DataIngestionArtifact:
    raw_data_dir:str 
    train_data_dir:str 
    test_data_dir:str 

@dataclass
class DataValidationArtifact:
    report_file_dir:str

@dataclass
class DataTransformationArtifact:
    transform_obj_dir: str
    transform_train_dir: str
    transform_test_dir:str
    target_encoder_dir:str

@dataclass
class ModelTrainerArtifact:...

@dataclass
class ModelEvaluationArtifact:...

@dataclass 
class ModelPusherArtifact:...