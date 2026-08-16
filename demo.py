from src.logger import logging
from src.exception import MyException
from src.data_access.fetch_mongodb_data import FetchMongoDBData
from src.pipeline.training_pipeline import TrainingPipeline
import sys
# print("heelo")

# testing of logger 
# logging.info("testing successfull")
# logging.error("error testing")

# testing of exception handler

# try:
#     a=1/0
# except Exception as e:
#     # raise MyException(e,sys) from e
#     raise MyException(e,sys) 

# data=FetchMongoDBData()
# data.export_collection_as_dataframe()

train_pip=TrainingPipeline()
res=train_pip.run_pipeline()
