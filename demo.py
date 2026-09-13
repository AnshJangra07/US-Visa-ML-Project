# from us_visa.logger import logging
# from us_visa.exception import USvisaException
# import sys

# logging.info("Welcome to out custom log")

# try:
#    a = 2/0
# except Exception as e:
#    raise USvisaException(e,sys)

# ----------------------------------------------------------
from us_visa.pipline.training_pipeline import TrainPipeline

obj = TrainPipeline()
obj.run_pipeline()