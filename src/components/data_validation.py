import os
import sys
from src.logger import logging
from src.exception import MyException
from src.utils.main_utils import read_yaml_file,read_csv_file,write_yaml_file
from src.constants import SCHEMA_FILE_PATH
from src.entity.artifact_entity import DataIngestionArtifacts,DataValidationArtifacts
from src.entity.config_entity import DataValidationConfig
import pandas as pd

class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifacts,data_validaiton_config:DataValidationConfig):
        try:
            self.schema_config=read_yaml_file(SCHEMA_FILE_PATH)
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validaiton_config=data_validaiton_config
        except Exception as e:
            raise MyException(e,sys)

    def validate_no_of_columns(self,df:pd.DataFrame)->bool:
        try:
            # check the no . of columns 
            status=(len(df.columns) == len(self.schema_config["columns"]))
            return status
        except Exception as e:
            raise MyException(e,sys)  

    def is_column_exist(self,df:pd.DataFrame)->bool:
        """this columns check if all nums and cat col exist"""
        try:
            logging.info("valdation cat/num col started ")
            num_cols=self.schema_config["numerical_columns"]
            cat_cols=self.schema_config["categorical_columns"]
            missing_num_cols=[]
            missing_cat_cols=[]
            # check for num cols
            for col in num_cols:
                if col not in df.columns:
                    missing_num_cols.append(col)

            if len(missing_num_cols)>0:
                logging.error(f"missing num cols are {missing_num_cols}")    

            for col in cat_cols:
                if col not in df.columns:
                    missing_cat_cols.append(col)

            if len(missing_cat_cols)>0:
                logging.error(f"missing cat cols are {missing_cat_cols}")

            if len(missing_num_cols)>0 or len(missing_cat_cols)>0:
                return False

            logging.info("valdation cat/num col ended ")
            return True
        except Exception as e:
            raise MyException(e,sys)  

    def initiate_data_validation(self)->DataValidationArtifacts:
        try:
            logging.info("started data validation")
            validaiton_error_message=""
            # read the train and test csv from the artifact/time_data_ingestion/ingested/train/test.csv
            train_file_path=self.data_ingestion_artifact.train_file_path
            test_file_path=self.data_ingestion_artifact.test_file_path

            # read teh csv file of train & test
            train_df=read_csv_file(train_file_path)
            test_df=read_csv_file(test_file_path)

            # check for all column exist
            train_check=self.validate_no_of_columns(train_df)
            if not train_check:
                validaiton_error_message+="columns are missing in train_df"
            else:
                logging.info("train_df has all columns")
            
            test_check=self.validate_no_of_columns(test_df)
            if test_check:
                logging.info("test_df has all columns")
            else:
                validaiton_error_message+="columns are missing in test_df"

            # validate column dtype for train and test 
            status=self.is_column_exist(train_df)
            if status:
                logging.info("all cat/num columns are present")
            else:
                validaiton_error_message+="some cat/num cols are missing in train_df"
                logging.error("some columns are missing in train_df")

            status=self.is_column_exist(test_df)
            if status:
                logging.info("all cat/num columns are present")
            else:
                validaiton_error_message+="some cat/num cols are missing in test_df"
                logging.error("some columsn are miissing in test_df")

            validation_status=len(validaiton_error_message)==0
            # create the object of data_valdation_artifact
            data_validation_artifact=DataValidationArtifacts(validation_status=validation_status,
                                          message=validaiton_error_message,
                                          validation_report_file_path=self.data_validaiton_config.validation_report_file_path)

            validation_report={
                "validation_status":validation_status,
                "message":validaiton_error_message.strip()
            }
            # now save this json validation_report instide the report.yaml file 
            # make sure the directory exsit 
            os.makedirs(os.path.dirname(self.data_validaiton_config.validation_report_file_path),exist_ok=True)
            write_yaml_file(self.data_validaiton_config.validation_report_file_path,validation_report,True)
            logging.info("data validation artifact created & saved to json file ")
            return data_validation_artifact
        except Exception as e:
            raise MyException(e,sys)