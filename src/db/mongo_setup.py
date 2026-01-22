from pymongo import MongoClient
from utils.config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client["chat_db"]
collection = db["conversations"]

def insert_conversation(doc):
    collection.insert_one(doc)
