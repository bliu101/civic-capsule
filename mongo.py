from pymongo import MongoClient
import os

MONGO_URI = os.environ.get("MONGODB_URI")
DB_NAME = os.environ.get("DB_NAME", "rocketchat")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

def get_users_collection():
    return db["users"]