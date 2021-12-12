from dotenv import load_dotenv
import os
from pymongo import MongoClient

try:
    load_dotenv()

    MONGO_URI = os.environ["MONGO_URI"]

    client = MongoClient(MONGO_URI)
    db = client["nhlelo"]
except:
    print("error loading env variable")
