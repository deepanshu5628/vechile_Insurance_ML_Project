import os 
import sys
import numpy as np 
import pandas as pd 
from src.logger import logging
from src.exception import MyException
from src.entity.config_entity import ModelTrainerConfig
from src.entity.artifact_entity import DataTransformationArtifacts
from src.entity.estimator import MyModel
from src.entity.artifact_entity import ClassificationMetricArtifact,ModelTrainerArtifacts
from src.utils.main_utils import load_numpy_arr_data,save_object,load_object
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,f1_score,precision_score,recall_score


class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig,data_transformation_artifact:DataTransformationArtifacts):
        try:
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact
        except Exception as e :
            raise MyException(e,sys)

    def get_model_object_and_report(self,train_arr:np.array,test_arr:np.array):
        try:
            x_train=train_arr[:,:-1]
            y_train=train_arr[:,-1]
            x_test=test_arr[:,:-1]
            y_test=test_arr[:,-1]

            logging.info("train_test split done")
            # train_test_split done
            trained_model=RandomForestClassifier(
                n_estimators=self.model_trainer_config.n_estimators,
                criterion=self.model_trainer_config.criterion,
                max_depth=self.model_trainer_config.max_depth,
                min_samples_split=self.model_trainer_config.min_sample_split,
                min_samples_leaf=self.model_trainer_config.min_sample_leaf,
                random_state=self.model_trainer_config.random_state
            )
            logging.info("model training going on !")
            trained_model.fit(x_train,y_train)
            logging.info("model training completed !")

            output=trained_model.predict(x_test)
            # metrics
            acc_sco=accuracy_score(y_test,output)
            f1_sco=f1_score(y_test,output)
            precision_sco=precision_score(y_test,output)
            recall_sco=recall_score(y_test, output)
            logging.info("creating metric artifact")
            classifcation_metric=ClassificationMetricArtifact(
                f1_score=f1_sco,
                precision_score=precision_sco,
                recall_score=recall_sco,
                accuracy_score=acc_sco
            )
            return trained_model, classifcation_metric
        except Exception as e :
            raise MyException(e,sys)

    def initiate_data_validation(self)->ModelTrainerArtifacts:
        try:
            # fetch the train_arr and test_arr (np)
            train_arr=load_numpy_arr_data(self.data_transformation_artifact.transformed_train_file_path)
            test_arr=load_numpy_arr_data(self.data_transformation_artifact.transformed_test_file_path)

            # train the model and get metrics report
            trained_model,classifcation_metric=self.get_model_object_and_report(train_arr=train_arr,test_arr=test_arr)

            # CHECK IF THE MODEL ACCURACY IS BETTER THEN THE THRESHHOLD
            # if accuracy_score(train_arr[:,-1],trained_model.predict(train_arr[:,:-1]))< self.model_trainer_config.expected_accuracy:
            if classifcation_metric.accuracy_score < self.model_trainer_config.expected_accuracy:
                logging.info("no model with score above the base score ")
                raise Exception("no model found with score above the base score ")
                
            # save the model at the given file path  with preprocessing object
            preprocessing_obj=load_object(self.data_transformation_artifact.transformed_object_file_path)
            my_model=MyModel(preprocessing_obj,trained_model)
            save_object(self.model_trainer_config.trained_model_file_path,my_model)
            logging.info("saving final model object that includes both  preprocessing and the trained model")

            # create & retrun the model_trainer_artifact 
            model_trainer_artifact=ModelTrainerArtifacts(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                metric_artifact=classifcation_metric
            )
            logging.info(f"model trainer artifact {model_trainer_artifact}")
            return model_trainer_artifact
        except Exception as e :
            raise MyException(e,sys)