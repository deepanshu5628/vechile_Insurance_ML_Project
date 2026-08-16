from dataclasses import dataclass
@dataclass
class DataIngestionArtifacts:
    train_file_path:str
    test_file_path:str

@dataclass
class DataValidationArtifacts:
    validation_status:bool
    message:str
    validation_report_file_path:str