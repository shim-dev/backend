import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_URI = os.getenv("MONGO_URI")
    MONGO_DB = os.getenv("MONGO_DB")

# MongoDB 연결
client = MongoClient(Config.MONGO_URI)
db = client[Config.MONGO_DB]

# 컬렉션
users = db["users"]
health_profiles = db["health_profiles"]