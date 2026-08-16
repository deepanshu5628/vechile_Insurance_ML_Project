import os 
import sys
from src.logger import logging
from src.exception import MyException
from src.entity.artifact_entity import DataTransformationArtifacts,DataIngestionArtifacts,DataValidationArtifacts
from src.entity.config_entity import DataTransformationConfig

class DataTransformation:
    def __init__(self,data_transformation_configs:DataTransformationConfig,data_ingestion_artifact:DataIngestionArtifacts,data_validation_artifact:DataValidationArtifacts):
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_transformation_configs=data_transformation_configs
            self.data_validation_artifact=data_validation_artifact
        except Exception as e :
            raise MyException(e,sys)


    def initiate_data_transformation(self)->DataTransformationArtifacts:
        try:
            if not  self.data_validation_artifact.validation_status:
                logging.error("validation status is false, feature store is not valid")
                raise Exception("validation status is false, feature store is not valid")
            # continue data transformation
            logging.info("data transformation initiated")
            logging.info("data transformation ended")

        except Exception as e :
            raise MyException(e,sys)