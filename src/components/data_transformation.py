import os 
import sys
import numpy as np 
import pandas as pd 
from src.logger import logging
from src.exception import MyException
from src.entity.artifact_entity import DataTransformationArtifacts,DataIngestionArtifacts,DataValidationArtifacts
from src.entity.config_entity import DataTransformationConfig
from src.utils.main_utils import read_csv_file ,read_yaml_file,save_numpy_arr_data,save_object
from src.constants import SCHEMA_FILE_PATH,TARGET_COLUMN

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from imblearn.combine import SMOTEENN
from sklearn.preprocessing import StandardScaler , MinMaxScaler
class DataTransformation:
    def __init__(self,data_transformation_configs:DataTransformationConfig,data_ingestion_artifact:DataIngestionArtifacts,data_validation_artifact:DataValidationArtifacts):
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_transformation_configs=data_transformation_configs
            self.data_validation_artifact=data_validation_artifact
            self.schema_config=read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e :
            raise MyException(e,sys)

    def get_data_transformer_object(self)->Pipeline:
        try:
            # we have to create a pipeline where we can apply tranforation
            # on num columns
            transformer=[
                ("num_standard",StandardScaler(),self.schema_config["num_features"]),
                ("min_max",MinMaxScaler(),self.schema_config["mm_columns"])
            ]
            preprocessor=ColumnTransformer(transformers=transformer,remainder="passthrough")

            # now creat the pipeline from it 
            final_pipeline=Pipeline(steps=[("scaling",preprocessor)])
            logging.info("Final Pipeline Ready")
            return final_pipeline
        except Exception as e :
            raise MyException(e,sys)

    def map_gender_column(self,df:pd.DataFrame)->pd.DataFrame:
        try:
            df["Gender"]=df["Gender"].map({"Male":0,"Female":1}).astype(int)
            return df
        except Exception as e:
            raise MyException(e,sys)

    def create_dummy_column(self,df:pd.DataFrame):
        try:
            df=pd.get_dummies(df,drop_first=True,dtype=int)
            return df
        except Exception as e :
            raise MyException(e,sys)

    def rename_column(self,df:pd.DataFrame):
        try:
            df=df.rename(columns={
                "Vehicle_Age_< 1 Year": "Vehicle_Age_lt_1_Year",
                "Vehicle_Age_> 2 Years": "Vehicle_Age_gt_2_Years"
            })

            for col in ["Vehicle_Damage_Yes"]:
                if col in df.columns:
                    df[col]=df[col].astype("int")
            return df
        except Exception as e:
            raise MyException(e,sys)

    def drop_id_column(self,df:pd.DataFrame):
        try:
            drop_col=self.schema_config["drop_columns"]
            if drop_col in df.columns:
                df=df.drop(drop_col,axis=1)
            return df
        except Exception as e:
            raise MyException(e,sys)

    def initiate_data_transformation(self)->DataTransformationArtifacts:
        try:
            logging.info("data transformation initiated")
            if not  self.data_validation_artifact.validation_status:
                logging.error("validation status is false, feature store is not valid")
                raise Exception("validation status is false, feature store is not valid")
            # continue data transformation
            logging.info("data validaation is done. starting data_Transformation")
            train_df=read_csv_file(self.data_ingestion_artifact.train_file_path)
            test_df=read_csv_file(self.data_ingestion_artifact.test_file_path)

            train_input_feature_df=train_df.drop(columns=[TARGET_COLUMN])
            train_output_feature_df=train_df[TARGET_COLUMN]

            test_input_feature_df=test_df.drop(columns=[TARGET_COLUMN])
            test_output_feature_df=test_df[TARGET_COLUMN]
            logging.info("x and y defined for both train & test df")

            # apply custom transfoation on input of both train and test
            train_input_feature_df=self.map_gender_column(df=train_input_feature_df)
            train_input_feature_df=self.create_dummy_column(df=train_input_feature_df)
            train_input_feature_df=self.rename_column(train_input_feature_df)
            train_input_feature_df=self.drop_id_column(df=train_input_feature_df)

            test_input_feature_df=self.map_gender_column(df=test_input_feature_df)
            test_input_feature_df=self.create_dummy_column(df=test_input_feature_df)
            test_input_feature_df=self.rename_column(test_input_feature_df)
            test_input_feature_df=self.drop_id_column(df=test_input_feature_df)
            logging.info("Custom transformation's applied to train & test data")

            logging.info("starting dataTransformation")
            preprocessor=self.get_data_transformer_object()
            logging.info("got the preprocessor object")
            logging.info("initilezed tranformation on training data ")
            train_input_feature_arr=preprocessor.fit_transform(train_input_feature_df)
            logging.info("initilezed tranformation on testing data ")
            test_input_feature_arr=preprocessor.transform(test_input_feature_df)
            logging.info("Transformation done end to end to Train&test df")

            logging.info("applying smoteenn for handling imbalance dataset")
            smt=SMOTEENN(sampling_strategy="minority")
            x_train,y_train=smt.fit_resample(train_input_feature_arr,train_output_feature_df)
            x_test,y_test=smt.fit_resample(test_input_feature_arr,test_output_feature_df)
            logging.info("smoteenn applied to train-test df")

            # now combine the transformed input features with target features
            train_arr=np.c_[x_train,np.array(y_train)]
            test_arr=np.c_[x_test,np.array(y_test)]
            logging.info("feature-target concatring is done ")

            # paths where we have to save files 
            train_file_save_path=self.data_transformation_configs.transformation_train_file_path
            test_file_save_path=self.data_transformation_configs.transformation_test_file_path
            object_save_path=self.data_transformation_configs.transformation_object_file_path

            # save the data
            save_numpy_arr_data(train_file_save_path,train_arr)
            save_numpy_arr_data(test_file_save_path, test_arr)
            save_object(object_save_path,preprocessor)

            logging.info("saveing transformed objects and files ")
            logging.info("data transformation completed successfully")

            return DataTransformationArtifacts(
                transformed_object_file_path=object_save_path,
                transformed_test_file_path=test_file_save_path,
                transformed_train_file_path=train_file_save_path,
            )

        except Exception as e :
            raise MyException(e,sys)