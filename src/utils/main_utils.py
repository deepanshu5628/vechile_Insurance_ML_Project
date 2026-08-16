import os 
import sys
import yaml
import pandas as pd
import numpy as np
import dill
from src.logger import logging
from src.exception import MyException


# fxn to read a yaml file 
def read_yaml_file(file_path:str)->dict:
    try:
        with open(file_path,"rb")as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e :
        raise MyException(e,sys)

def read_csv_file(file_path:str)->pd.DataFrame:
    try:
        with open(file_path,"r")as csv_file:
            return pd.read_csv(csv_file)
    except Exception as e:
        raise Exception(e,sys)

# write a yaml file 
def write_yaml_file(file_path:str,content:object,replace:bool=False)->None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        # make the dir
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"w")as yaml_file:
            yaml.dump(content,yaml_file)
    except Exception as e:
        raise MyException(e,sys)


def load_objects(file_path:str)->object:
    try:
        with open(file_path,"rb") as file_obj:
            obj=dill.load(file_obj)
            return obj
    except Exception as e:
        raise MyException(e,sys)


def save_numpy_arr_data(file_path:str,arr:np.array)->None:
    try:
        # make the dir if not exsit 
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"wb")as file_arr:
            np.save(arr=arr,file=file_arr)
    except Exception as e :
        raise MyException(e,sys)

# laod numpy arr data 
def load_numpy_arr_data(file_path:str)->np.array:
    try:
        with open(file_path,"rb")as file:
            arr=np.load(file)
            return arr
    except Exception as e:
        raise MyException(e,sys)