import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

mongo_uri = os.getenv("MONGO_URI")
mongo_db_name = os.getenv("MONGO_DB")

client = MongoClient(mongo_uri)
db = client[mongo_db_name]

users = db["users"]
health_profiles = db["health_profiles"]
print("✅ MONGO_URI:", mongo_uri)
