from dotenv import load_dotenv
import logging
import os
from pymongo import MongoClient

logging.debug("===== TRYING TO LOAD ENV VARS =====")
logging.debug(f"ENV VARS === {os.environ}")
print("===== THIS IS ONLY A TEST =====")

try:
    load_dotenv()

    MONGO_URI = os.environ["MONGO_URI"]

    client = MongoClient(MONGO_URI)
    db = client["nhlelo"]
except:
    logging.debug("error loading env variable")
