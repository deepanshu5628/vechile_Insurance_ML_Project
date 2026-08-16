import os
from dataclasses import dataclass
from src.constants import (PIPELINE_NAME ,TIMESTAMP,ARTIFACT_DIR,DATA_INGESTION_DIR_NAME,DATA_INGESTION_COLLECTION_NAME,
                           DATA_INGESTION_TEST_TRAIN_SPLIT_RATIO,DATA_INGESTION_FEATURE_STORE_DIR,DATA_INGESTION_INGESTED_DIR,
                           FILE_NAME,TRAIN_FILE_NAME,TEST_FILE_NAME,DATA_VALIDATION_DIR_NAME,DATA_VALIDATION_REPORT_FILE_NAME,
                           DATA_TRANSFORMATION_DIR_NAME,DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,
                           PREPROCSSING_OBJECT_FILE_NAME)

@dataclass
class TrainingPipelineConfig:
    pipeline_name:str=PIPELINE_NAME
    artifact_dir:str=os.path.join(ARTIFACT_DIR,TIMESTAMP)   #artifcat/timestamp/
    timestamp:str=TIMESTAMP


training_pipeline_config:TrainingPipelineConfig=TrainingPipelineConfig()

@dataclass
class DataIngestionConfig:
    data_ingestion_dir:str=os.path.join(training_pipeline_config.artifact_dir,DATA_INGESTION_DIR_NAME) #artifcat/timestamp/data_ingestion
    feature_store_file_path:str=os.path.join(data_ingestion_dir,DATA_INGESTION_FEATURE_STORE_DIR,FILE_NAME)  #artifcat/timestamp/data_ingestion/feature_store/filename
    training_file_path:str=os.path.join(data_ingestion_dir,DATA_INGESTION_INGESTED_DIR,TRAIN_FILE_NAME)#artifcat/timestamp/data_ingestion/ingested/train.csv
    testing_file_path:str=os.path.join(data_ingestion_dir,DATA_INGESTION_INGESTED_DIR,TEST_FILE_NAME)
    train_test_split_ratio:float=DATA_INGESTION_TEST_TRAIN_SPLIT_RATIO
    collection_name:str=DATA_INGESTION_COLLECTION_NAME

@dataclass
class DataValidationConfig:
    data_validation_dir:str=os.path.join(training_pipeline_config.artifact_dir ,DATA_VALIDATION_DIR_NAME)
    validation_report_file_path:str=os.path.join(data_validation_dir,DATA_VALIDATION_REPORT_FILE_NAME)

@dataclass
class DataTransformationConfig:
    data_transformation_dir:str=os.path.join(training_pipeline_config.artifact_dir,DATA_TRANSFORMATION_DIR_NAME)
    transformation_train_file_path:str=os.path.join(data_transformation_dir,DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,TRAIN_FILE_NAME.replace("csv","npy"))
    transformation_test_file_path:str=os.path.join(data_transformation_dir,DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR,TEST_FILE_NAME.replace("csv","npy"))
    transformation_object_file_path:str=os.path.join(data_transformation_dir,DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR,PREPROCSSING_OBJECT_FILE_NAME)

