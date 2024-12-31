# database_module.py
import pymongo
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=30000)
db = client['health_db']
users_collection = db['users']

def save_user_data(data):
    users_collection.insert_one(data)


def get_user_data(user_id):
    return users_collection.find_one({"user_id": user_id})
