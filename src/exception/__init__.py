import sys 
import logging

def error_message_details(error:Exception,error_details:sys)->str:
    _,_,exc_tb =error_details.exc_info()

    # get the filename where the error has been occured
    file_name=exc_tb.tb_frame.f_code.co_filename

    # create a proper error with file_name, line_no, and error message
    line_no=exc_tb.tb_lineno
    error_message=f"Error occured in python script[{file_name}] at line no[{line_no}]:{str(error)}"

    #log the error 
    logging.error(error_message)

    #return the error message
    return error_message


class MyException(Exception):
    def __init__(self,error:str,error_details:sys):
        # call the base constructor (Exception) and give it the main eror
        super().__init__(error)

        # format the error with proper message
        self.error=error_message_details(error,error_details)

    def __str__(self)->str:
        return self.error