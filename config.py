import os
from pymongo import MongoClient
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 환경 변수에서 MongoDB 연결 정보 불러오기
mongo_uri = os.getenv("MONGO_URI")
mongo_db_name = os.getenv("MONGO_DB")

# MongoDB 클라이언트 및 DB 연결
client = MongoClient(mongo_uri)
db = client[mongo_db_name]

users = db["users"]
health_profiles = db["health_profiles"]
records = db["records"]
water_records = db["water_records"]
sleep_hours = db["sleep_hours"]
notices_col = db["notices"]
events_col = db["events"]
inquiry_col = db["inquiries"]
quit_reasons_col = db["quit_reasons"]
images_col = db["images"]
bookmarks = db["bookmarks"]
recipes = db["recipes"]
