import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

mongo_uri = os.getenv("MONGO_URI")
mongo_db_name = os.getenv("MONGO_DB")

client = MongoClient(mongo_uri)
db = client[mongo_db_name]

records = db['records']
water_records = db['water_records']
sleep_hours = db['sleep_hours']
users = db['users']
notices_col = db["notices"]
events_col = db["events"]
inquiry_col = db['inquiries']
quit_reasons_col = db['quit_reasons']
images_col = db['images']
bookmarks = db['bookmarks']
recipes = db['recipes']
