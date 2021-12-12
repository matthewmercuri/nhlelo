from dotenv import load_dotenv
import logging
import os
from pymongo import MongoClient

print("===== TRYING TO LOAD ENV VARS =====")
print(f"ENV VARS === {os.environ}")
print("===== THIS IS ONLY A TEST =====")

try:
    load_dotenv()

    MONGO_URI = os.environ["MONGO_URI"]

    client = MongoClient(MONGO_URI)
    db = client["nhlelo"]
except:
    logging.debug("error loading env variable")
