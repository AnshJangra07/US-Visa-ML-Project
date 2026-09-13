import os
from dotenv import load_dotenv
from datetime import date
load_dotenv()
MongoDB_URL = os.getenv("MONGODB_URL")


DATABASE_NAME = "US_VISA"

COLLECTION_NAME = "VISA_DATA"

MONGODB_URL_KEY = MongoDB_URL

PIPELINE_NAME : str = "usvisa"
ARTIFACT_DIR : str = "artifact"

MODEL_FILE_NAME = "model.pkl"


"""
Data Ingestion related constant start with DATA_INGESTION VAR NAME
"""
DATA_INGESTION_COLLECTION_NAME: str = "visa_data"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2