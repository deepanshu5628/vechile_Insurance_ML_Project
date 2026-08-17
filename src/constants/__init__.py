import os
from datetime import datetime

# for mongodb connection
DATABASE_NAME="vehicle_insurance_database"
MONGODB_URI_KEY="mongodb+srv://d2810201_db_user:KRHu85jyWwlXanxa@clusterai.5di8rsk.mongodb.net/?appName=clusterai"


PIPELINE_NAME:str=""
ARTIFACT_DIR:str="artifacts"
TIMESTAMP:str=datetime.now().strftime("%m_%d_%Y_%H_%M_%S")

MODEL_FILE_NAME="model.pkl"
PREPROCSSING_OBJECT_FILE_NAME = "preprocessing.pkl"
TARGET_COLUMN:str="Response"

FILE_NAME:str="data.csv"
TRAIN_FILE_NAME:str="train.csv"
TEST_FILE_NAME:str="test.csv"
SCHEMA_FILE_PATH:str=os.path.join("config","schema.yaml")


""" 
Data ingestion related constants start with DATA_INGESTION VAR NAME
"""
DATA_INGESTION_COLLECTION_NAME:str="vehicle_insurance_collection"
DATA_INGESTION_DIR_NAME:str="data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR:str="feature_store"
DATA_INGESTION_INGESTED_DIR:str="ingested"
DATA_INGESTION_TEST_TRAIN_SPLIT_RATIO:float=0.25

"""
DATA VALIDATION RELATED CONSTANTS STARTS WITH DATA_VALIDATION VAR NAME
"""
DATA_VALIDATION_DIR_NAME:str="data_validation"
DATA_VALIDATION_REPORT_FILE_NAME:str="report.yaml" 

"""
DATA TRANSFORMATIONIN RELATED CONSTANTS STARTS WITH DATA_TRANSFORMATION VAR NAME
"""
DATA_TRANSFORMATION_DIR_NAME:str="data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR:str="transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR:str="transformed_object"


"""
MODEL TRAINER related constant start with MODEL_TRAINER var name
"""
MODEL_TRAINER_DIR_NAME: str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR: str = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_NAME: str = "model.pkl"
MODEL_TRAINER_EXPECTED_SCORE: float = 0.6
MODEL_TRAINER_MODEL_CONFIG_FILE_PATH: str = os.path.join("config", "model.yaml")
MODEL_TRAINER_N_ESTIMATORS=200
MODEL_TRAINER_MIN_SAMPLES_SPLIT: int = 7
MODEL_TRAINER_MIN_SAMPLES_LEAF: int = 6
MIN_SAMPLES_SPLIT_MAX_DEPTH: int = 10
MIN_SAMPLES_SPLIT_CRITERION: str = 'entropy'
MIN_SAMPLES_SPLIT_RANDOM_STATE: int = 101