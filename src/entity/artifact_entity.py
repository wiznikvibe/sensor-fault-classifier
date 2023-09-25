from dataclasses import dataclass 

@dataclass
class DataIngestionArtifact:
    raw_data_dir:str 
    train_data_dir:str 
    test_data_dir:str 