from src.exception import MyException
from src.logger import logging
from src.constants import MONGODB_URI_KEY,DATABASE_NAME
import sys
import os
import certifi
import pymongo
# this file has the logic of connecting with mongodb database

ca=certifi.where()
class MongoDBClient:
    client=None
    def __init__(self,database_name:str=DATABASE_NAME)->None:
        try:
            if MongoDBClient.client is None:
                mongo_db_url=MONGODB_URI_KEY
                if mongo_db_url is None:
                    logging.error("env varialbe is not set ")
                    raise Exception(f"Environment variable {mongo_db_url} is not set ")

                # estblish a new mongodb connection
                MongoDBClient.client=pymongo.MongoClient(mongo_db_url,tlsCAFile=ca) 

            self.client=MongoDBClient.client
            self.database=self.client[database_name]
            self.database_name=database_name
            logging.info("mongodb connection successfull")
        except Exception as e:
            raise MyException(e,sys) 