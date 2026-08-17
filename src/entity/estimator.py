import os
import sys
from src.exception import MyException
from sklearn.pipeline import Pipeline
# import object
import pandas as pd
class MyModel:
    def __init__(self,pipeline_object:Pipeline,trained_model_object:object):
        try:
            self.pipeline_object=pipeline_object
            self.trained_model_object=trained_model_object
        except Exception as e:
            raise MyException(e,sys)

    def predict(self,df:pd.DataFrame):
        try:
            pass
        except Exception as e:
            raise MyException(e,sys)
