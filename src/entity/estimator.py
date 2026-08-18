import sys
from src.exception import MyException
from sklearn.pipeline import Pipeline
import numpy as np 
class MyModel:
    def __init__(self,pipeline_object:Pipeline,trained_model_object:object):
        try:
            self.pipeline_object=pipeline_object
            self.trained_model_object=trained_model_object
        except Exception as e:
            raise MyException(e,sys)

    def predict(self,npy_arr:np.array):
        try:
            output=self.trained_model_object.predict(npy_arr)
            return output
        except Exception as e:
            raise MyException(e,sys)
