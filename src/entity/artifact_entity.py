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

@dataclass
class DataTransformationArtifacts:
    transformed_train_file_path:str
    transformed_test_file_path:str
    transformed_object_file_path:str

@dataclass
class ClassificationMetricArtifact:
    f1_score:float
    precision_score:float
    recall_score:float
    accuracy_score:float

@dataclass 
class ModelTrainerArtifacts:
    trained_model_file_path:str
    metric_artifact:ClassificationMetricArtifact