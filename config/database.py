from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()


MONGODB_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGODB_URI)

db = client.sim

collection_name = db["sim"]

