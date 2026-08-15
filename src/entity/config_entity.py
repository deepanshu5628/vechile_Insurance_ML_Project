import os
from dataclasses import dataclass
from src.constants import (PIPELINE_NAME ,TIMESTAMP,ARTIFACT_DIR,DATA_INGESTION_DIR_NAME,DATA_INGESTION_COLLECTION_NAME,
                           DATA_INGESTION_TEST_TRAIN_SPLIT_RATIO,DATA_INGESTION_FEATURE_STORE_DIR,DATA_INGESTION_INGESTED_DIR,
                           FILE_NAME,TRAIN_FILE_NAME,TEST_FILE_NAME)

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
