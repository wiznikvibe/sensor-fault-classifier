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
class ModelTrainerArtifact:
    model_path: str
    f1_train_score: str 
    f1_test_score: str 

@dataclass
class ModelEvaluationArtifact:
    is_model_accepted: bool 
    improved_accuracy: float 

@dataclass 
class ModelPusherArtifact:...