import os 
import sys
import numpy as np 
import pandas as pd 

from src.exception import MyException
from src.logger import logging
from src.configurations.mongodb_connection import MongoDBClient
from src.constants import DATABASE_NAME 

class FetchMongoDBData():
    """
    the work of this class is to fetch the data 
    from mongodb and strore it a pandas dataframe
    """
    def __init__(self)->None:
        # initilze the mongodb connection
        try:
            self.mongo_client=MongoDBClient(database_name=DATABASE_NAME)
        except Exception as e:
            raise MyException(e,sys)

    def export_collection_as_dataframe(self,collection_name:str,database_name:Optional[str]=None)->pd.DataFrame:
        try:
            # fetch the spefic or default collection from the db 
            if database_name is None:
                collection=self.mongo_client.database[collection_name]
            else:
                collection=self.mongo_client[database_name][collection_name]
            print("fetching data from the db")
            df=pd.DataFrame(list(collection.find()))
            print(f"fetched data with size {len(df)}")
            if "_id" in df.columns.to_list():
                df=df.drop(columns=["_id"])
            df.replace({"na":np.nan},inplace=True)
            return df
        except Exception as e:
            raise MyException(e,sys)
