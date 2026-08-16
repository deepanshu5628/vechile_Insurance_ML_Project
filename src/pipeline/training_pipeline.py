import sys
from src.exception import MyException
from src.logger import logging
from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.entity.config_entity import DataIngestionConfig,DataValidationConfig
from src.entity.artifact_entity import DataIngestionArtifacts,DataValidationArtifacts

class TrainingPipeline:
    def __init__(self):
        self.data_ingestion_configs=DataIngestionConfig()
        self.data_validation_configs=DataValidationConfig()

    def start_data_ingestion(self)->DataIngestionArtifacts:
        """this method is responsible for running the data ingestion component"""
        try:
            logging.info("Data ingestion started")
            data_ingestion=DataIngestion(data_ingestion_config=self.data_ingestion_configs)
            data_ingestion_artifacts=data_ingestion.initiate_data_ingestion()
            logging.info("exited the start_data_ingestion method of Training pipeline class")
            return data_ingestion_artifacts
        except Exception as e:
            raise MyException(e,sys)

    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifacts)->DataValidationArtifacts:
        try:
            logging.info("Data Validaiton Started")
            data_validation=DataValidation(data_ingestion_artifact,self.data_validation_configs)
            data_validation_artifct=data_validation.initiate_data_validation()
            logging.info("Data Validaiton Ended")
            return data_validation_artifct
        except Exception as e:
            raise MyException(e,sys)


    def run_pipeline(self)->None:
        """this method is responcible for running the complete pipeline"""
        try:
            logging.info("started the training pipeline")
            data_ingestion_artifact=self.start_data_ingestion()
            data_validation_artifact=self.start_data_validation(data_ingestion_artifact)
            logging.info("ending of the training pipeline")
        except Exception as e:
            raise MyException(e,sys)