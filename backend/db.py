from dotenv import load_dotenv
import logging
import os
from pymongo import MongoClient

try:
    load_dotenv()

    MONGO_URI = os.environ["MONGO_URI"]

    client = MongoClient(MONGO_URI)
    db = client["nhlelo"]
except:
    logging.debug("error loading env variable")
