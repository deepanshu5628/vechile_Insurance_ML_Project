import logging
import os
from from_root import from_root
from datetime import datetime
from logging.handlers import RotatingFileHandler

LOG_DIR="logs"   #parent folder name 
LOG_FILE=f"{datetime.now().strftime("%m_%d_%Y_%H_%M_%S")}.log" #filename
BACKUP_COUNT=3
MAX_LOG_SIZE=5*1024*1024   #max file size ie. 5MB

# log dir path
log_dir_path=os.path.join(from_root(),LOG_DIR)
os.makedirs(log_dir_path,exist_ok=True)  #make the logs dir if not exist
log_file_path=os.path.join(log_dir_path,LOG_FILE)   #file_path herd log filename is unique

def configure_logger():
    """configure the logger"""
    # create a custom logger
    logger=logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # log formatter
    log_formatter=logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # console handler
    console_handler=logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(log_formatter)

    # rotating_file handler
    rotating_file_handler=RotatingFileHandler(log_file_path,maxBytes=MAX_LOG_SIZE,backupCount=BACKUP_COUNT)
    rotating_file_handler.setLevel(logging.DEBUG)
    rotating_file_handler.setFormatter(log_formatter)

    # add both the handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(rotating_file_handler)

configure_logger()
    


