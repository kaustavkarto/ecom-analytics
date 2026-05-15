from pymongo import MongoClient
from app.core.config import MONGO_URI, MONGO_DATABASE

client = MongoClient(MONGO_URI)
db = client[MONGO_DATABASE]

def get_events_collection():
    return db['events']