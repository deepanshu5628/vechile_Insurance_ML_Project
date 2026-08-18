import os 
import sys
import pandas as pd 
from src.exception import MyException
from src.logger import logging
from src.entity.artifact_entity import DataIngestionArtifacts
from src.entity.config_entity import DataIngestionConfig
from src.data_access.fetch_mongodb_data import FetchMongoDBData 
from sklearn.model_selection import train_test_split


class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            # ingest the DataIngestion Configurations from the congig_entity.py
            self.data_ingestion_configs=data_ingestion_config
        except Exception as e:
            raise MyException(e,sys)

    def export_data_into_feature_store(self)->pd.DataFrame:
        """
        fetch data from mongodb and store it in a csv file
        output_path: 
        """
        try:
            # fetch the data from mongodb
            fetch_data=FetchMongoDBData()
            df=fetch_data.export_collection_as_dataframe(collection_name=self.data_ingestion_configs.collection_name)
            logging.info(f"the shape of imported df is {df.shape}")
            # save df as a csv file into folder #artifcat/timestamp/data_ingestion/feature_store/filename
            feature_store_file_path=self.data_ingestion_configs.feature_store_file_path
            dir_path=os.path.dirname(feature_store_file_path)
            # make this directory if not exist 
            os.makedirs(dir_path,exist_ok=True)  #this will create a folder called feature_store
            logging.info(f"saving exported data to feature store file path :{feature_store_file_path}")
            df.to_csv(feature_store_file_path,index=False,header=True)
            return df
        except Exception as e:
            raise MyException(e,sys) 

    def split_data_as_train_test(self,dataFrame:pd.DataFrame)->None:
        """
        this fxn will split the data into training and testting and store 
        on the output path:->
        """
        try:
            train_set,test_set=train_test_split(dataFrame,test_size=self.data_ingestion_configs.train_test_split_ratio,random_state=self.data_ingestion_configs.random_state)
            logging.info("performed train& test split ration on the data ")
            file_path=self.data_ingestion_configs.training_file_path

            #find the directory name and create it if  it not exist
            dir_path=os.path.dirname(file_path)
            os.makedirs(dir_path,exist_ok=True)
            # now create the csv file on the path
            logging.info("exporting traing&test file ")
            train_set.to_csv(self.data_ingestion_configs.training_file_path,index=False,header=True)
            test_set.to_csv(self.data_ingestion_configs.testing_file_path,index=False,header=True)
            logging.info("exported traing & test files")
        except Exception as e:
            raise MyException(e,sys)

    def initiate_data_ingestion(self)->DataIngestionArtifacts:
        """
        combine both fxn and return the path of exported file of train & test
        """
        try:
            data=self.export_data_into_feature_store()
            logging.info("got the dataframe from mongodb")
            self.split_data_as_train_test(data)
            logging.info("perfromed the train test split on the data ")
            logging.info("exitted the initiate_data_ingestion from data_ingestion class")

            data_ingestion_artifact=DataIngestionArtifacts(train_file_path=self.data_ingestion_configs.training_file_path,test_file_path=self.data_ingestion_configs.testing_file_path)
            logging.info(f"data ingestion artifact : {data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise MyException(e,sys)
