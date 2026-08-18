import sys
from src.exception import MyException
from src.logger import logging

# components
from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.components.model_evaluation import ModelEvaluation
from src.components.model_pusher import ModelPusher

# config entity
from src.entity.config_entity import (DataIngestionConfig,
                                      DataValidationConfig,
                                      DataTransformationConfig,
                                      ModelTrainerConfig,
                                      ModelEvaluationConfig,
                                      ModelPusherConfg)

# artifact entity
from src.entity.artifact_entity import (DataIngestionArtifacts,
                                        DataValidationArtifacts,
                                        DataTransformationArtifacts,
                                        ModelTrainerArtifacts,
                                        ModelEvaluationArtifacts,
                                        ModelPusherArtifacts)

class TrainingPipeline:
    def __init__(self):
        try:
            self.data_ingestion_configs=DataIngestionConfig()
            self.data_validation_configs=DataValidationConfig()
            self.data_transformation_configs=DataTransformationConfig()
            self.model_trainer_configs=ModelTrainerConfig()
            self.model_evaluation_configs=ModelEvaluationConfig()
            self.model_pusher_configs=ModelPusherConfg()
        except Exception as e:
            raise MyException(e,sys)

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
            logging.info("---------------------------------------------------------------")
            logging.info("Data Validaiton Started")
            data_validation=DataValidation(data_ingestion_artifact,self.data_validation_configs)
            data_validation_artifct=data_validation.initiate_data_validation()
            logging.info("Data Validaiton Ended")
            return data_validation_artifct
        except Exception as e:
            raise MyException(e,sys)

    def start_data_transformation(self,data_validation_artifact:DataValidationArtifacts,data_ingestion_artifact:DataIngestionArtifacts)->DataTransformationArtifacts:
        try:
            logging.info("---------------------------------------------------------------")
            logging.info("Data transformation started")
            data_transformation=DataTransformation(self.data_transformation_configs,data_ingestion_artifact,data_validation_artifact)
            data_transformation_artifact=data_transformation.initiate_data_transformation()
            logging.info("Data transformation Ended")
            return data_transformation_artifact
        except Exception as e:
            raise MyException(e,sys)

    def start_model_trainer(self,data_tranformation_artifact:DataTransformationArtifacts)->ModelTrainerArtifacts:
        try:
            logging.info("---------------------------------------------------------------")
            logging.info("Model Training Started") 
            model_trainer=ModelTrainer(self.model_trainer_configs,data_tranformation_artifact)
            model_trainer_artifact=model_trainer.initiate_model_trainer()
            logging.info("Model Training Ended") 
            return model_trainer_artifact
        except Exception as e:
            raise MyException(e,sys)

    def start_model_evaluation(self,model_trainer_artifact:ModelTrainerArtifacts,data_tranformation_artifact:DataTransformationArtifacts)->ModelEvaluationArtifacts:
        try:
            logging.info("---------------------------------------------------------------")
            logging.info("Model Evaluation Started") 
            model_evaluation=ModelEvaluation(model_trainer_artifact,self.model_evaluation_configs,data_tranformation_artifact)
            model_evaluation_artifact=model_evaluation.initiate_model_evaluation()
            logging.info("Model Evaluation Ended") 
            return model_evaluation_artifact
        except Exception as e:
            raise MyException(e, sys)

    def start_model_pusher(self,model_evaluation_artifact:ModelEvaluationArtifacts)->ModelPusherArtifacts:
        try:
            logging.info("---------------------------------------------------------------")
            logging.info("Model Pusher Started")
            model_pusher=ModelPusher(self.model_pusher_configs,model_evaluation_artifact)
            model_pusher_artifact=model_pusher.initiate_model_pusher()
            logging.info(f"Model Pusher Ended {model_pusher_artifact}")
            return model_pusher_artifact
        except Exception as e:
            raise MyException(e,sys)
        
    def run_pipeline(self)->None:
        """this method is responcible for running the complete pipeline"""
        try:
            logging.info("started the training pipeline")
            data_ingestion_artifact=self.start_data_ingestion()
            data_validation_artifact=self.start_data_validation(data_ingestion_artifact)
            data_tranformation_artifact=self.start_data_transformation(data_validation_artifact,data_ingestion_artifact)
            model_trainer_artifact=self.start_model_trainer(data_tranformation_artifact)
            model_evaluation_artifact=self.start_model_evaluation(model_trainer_artifact,data_tranformation_artifact)
            # check if model is accepted or not 
            if not model_evaluation_artifact.is_model_accepted:
                logging.info("Model not accepted")
                return None
            model_pusher_artifacts=self.start_model_pusher(model_evaluation_artifact)
            logging.info("ending of the training pipeline")
            return model_pusher_artifacts
        except Exception as e:
            raise MyException(e,sys)