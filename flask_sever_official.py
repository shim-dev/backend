from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import send_file
import io





app = Flask(__name__)
CORS(app)

# MongoDB 연결
client = MongoClient('mongodb+srv://20222640:1234@user.kxemihr.mongodb.net/')
db = client['app_database']
records = db['records']
water_records = db['water_records']
sleep_hours = db['sleep_hours']
users = db['users']
notices_col = db["notices"]
events_col = db["events"]
inquiry_col = db['inquiries']
quit_reasons_col = db['quit_reasons']
images_col = db['images']



@app.route('/insert_record', methods=['POST'])
def insert_record():
    data = request.json
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id 누락!'}), 400
    records.update_one(
        {
            'user_id': user_id,
            'date': data['date'],
            'mealType': data['mealType'],
            'name': data['name']
        },
        {'$set': data}, upsert=True
    )
    return jsonify({'status': 'success'})

@app.route('/get_records', methods=['GET'])
def get_records():
    user_id = request.args.get('user_id')
    date = request.args.get('date')
    mealType = request.args.get('mealType')
    if not user_id:
        return jsonify({'error': 'user_id 누락!'}), 400
    result = list(records.find({'user_id': user_id, 'date': date, 'mealType': mealType}))
    for doc in result:
        doc['_id'] = str(doc['_id'])
    return jsonify(result)

@app.route('/delete_record', methods=['DELETE'])
def delete_record():
    record_id = request.args.get('id')
    user_id = request.args.get('user_id')
    if not record_id or not user_id:
        return jsonify({'error': 'No id or user_id provided'}), 400
    try:
        result = records.delete_one({'_id': ObjectId(record_id), 'user_id': user_id})
        if result.deleted_count == 1:
            return jsonify({'status': 'deleted'})
        else:
            return jsonify({'error': 'Record not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/update_record', methods=['PUT'])
def update_record():
    data = request.json
    record_id = data.get('_id')
    user_id = data.get('user_id')
    if not record_id or not user_id:
        return jsonify({'error': 'No _id or user_id provided'}), 400
    update_data = {k: v for k, v in data.items() if k != '_id'}
    try:
        result = records.update_one(
            {'_id': ObjectId(record_id), 'user_id': user_id},
            {'$set': update_data}
        )
        if result.matched_count == 1:
            return jsonify({'status': 'updated'})
        else:
            return jsonify({'error': 'Record not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/save_water', methods=['POST'])
def save_water():
    data = request.json
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id 누락!'}), 400
    water_records.update_one(
        {'user_id': user_id, 'date': data['date']},
        {'$set': {'cups': data['cups']}},
        upsert=True
    )
    return jsonify({'status': 'success'})

@app.route('/get_water', methods=['GET'])
def get_water():
    user_id = request.args.get('user_id')
    date = request.args.get('date')
    if not user_id:
        return jsonify({'error': 'user_id 누락!'}), 400
    result = water_records.find_one({'user_id': user_id, 'date': date}, {'_id': 0})
    return jsonify(result if result else {'cups': 0})

@app.route('/insert_or_update_sleep', methods=['POST'])
def insert_or_update_sleep():
    data = request.json
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id 누락!'}), 400
    sleep_hours.update_one(
        {'user_id': user_id, 'date': data['date']},
        {'$set': {'hours': data['hours']}},
        upsert=True
    )
    return jsonify({'status': 'success'})

@app.route('/get_sleep', methods=['GET'])
def get_sleep():
    user_id = request.args.get('user_id')
    date = request.args.get('date')
    if not user_id:
        return jsonify({'error': 'user_id 누락!'}), 400
    result = sleep_hours.find_one({'user_id': user_id, 'date': date}, {'_id': 0})
    return jsonify(result if result else {'hours': 0})

@app.route('/get_all_records')
def get_all_records():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id 누락!'}), 400
    records_list = list(records.find({'user_id': user_id}))
    for r in records_list:
        r['_id'] = str(r['_id'])
    return jsonify(records_list)

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = users.find_one({'email': email})
    if user and check_password_hash(user['password'], password):  # hash 비교!
        return jsonify({
            'user_id': str(user['_id']),
            'nickname': user.get('nickname', ''),
            'email': user.get('email', '')
        }), 200
    else:
        return jsonify({'error': '이메일 또는 비밀번호가 올바르지 않습니다.'}), 401


# 회원가입 실헙실 두구두구
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    email = data.get('email')
    nickname = data.get('nickname')
    password = data.get('password')

    if users.find_one({'email': email}):
        return jsonify({'error': '이미 존재하는 이메일입니다.'}), 400

    hashed_pw = generate_password_hash(password)  # 해시로 변환!
    result = users.insert_one({
        'email': email,
        'nickname': nickname,
        'password': hashed_pw,
    })
    return jsonify({'message': '회원가입 성공!', 'user_id': str(result.inserted_id), 'nickname': nickname, 'email' : email}), 200



# 닉네임 조회 
@app.route('/get_nickname', methods=['GET'])
def get_nickname():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id 누락!'}), 400
    user = users.find_one({'_id': ObjectId(user_id)})
    if user:
        return jsonify({'nickname': user.get('nickname', '')}), 200
    else:
        return jsonify({'error': '사용자를 찾을 수 없음'}), 404


# 닉네임 수정
@app.route('/update_nickname', methods=['POST'])
def update_nickname():
    data = request.json
    user_id = data.get('user_id')
    new_nickname = data.get('nickname')
    if not user_id or not new_nickname:
        return jsonify({'error': 'user_id 또는 nickname 누락!'}), 400
    result = users.update_one(
        {'_id': ObjectId(user_id)},
        {'$set': {'nickname': new_nickname}}
    )
    if result.matched_count:
        return jsonify({'status': 'updated'}), 200
    else:
        return jsonify({'error': '사용자를 찾을 수 없음'}), 404

# 공지사항 서버에서 받아오기
@app.route('/get_notices', methods=['GET'])
def get_notices():
    notices = []
    for doc in notices_col.find({}, {"_id": 0}):  # _id는 빼고 전달
        notices.append(doc)
    return jsonify(notices)

# 이벤트 서버에서 받아오기
@app.route('/get_events', methods=['GET'])
def get_events():
    events = []
    for doc in events_col.find({}, {"_id": 0}):  # _id 제외
        events.append(doc)
    return jsonify(events)

# 문의 등록 (POST)
@app.route('/insert_inquiry', methods=['POST'])
def insert_inquiry():
    data = request.get_json()
    user_id = data.get('user_id')
    title = data.get('title')
    content = data.get('content')
    date = data.get('date')
    image_ids = data.get('image_ids', [])  # 배열로 받음

    if not (user_id and title and content and date):
        return jsonify({'error': '필수 데이터 누락'}), 400

    doc = {
        'user_id': user_id,
        'title': title,
        'content': content,
        'date': date,
        'created_at': datetime.now(),
        'image_ids': image_ids  # 여기!!
    }
    result = inquiry_col.insert_one(doc)
    return jsonify({'result': 'success', 'inquiry_id': str(result.inserted_id)})

# 이미지 파일 업로드 실험실
@app.route('/upload_image', methods=['POST'])
def upload_image():
    user_id = request.form.get('user_id')
    file = request.files.get('image')
    if not user_id or not file:
        return jsonify({'error': 'user_id 또는 이미지 누락'}), 400

    # 이미지 파일을 바이너리로 저장 (권장: GridFS, 여기선 간단하게 컬렉션에 저장)
    image_bytes = file.read()
    doc = {
        'user_id': user_id,
        'image': image_bytes,
        'created_at': datetime.now()
    }
    result = images_col.insert_one(doc)
    return jsonify({'image_id': str(result.inserted_id)}), 200

# 이미지 보기 api
@app.route('/get_image/<image_id>')
def get_image(image_id):
    img_doc = db['images'].find_one({'_id': ObjectId(image_id)})
    if not img_doc or 'image' not in img_doc:
        return 'Not found', 404
    # png, jpg 등 실제 확장자에 따라 변경
    return send_file(
        io.BytesIO(img_doc['image']),
        mimetype='image/png'  # jpg라면 'image/jpeg'
    )

# 문의 내역 조회 (GET)
@app.route('/get_inquiries', methods=['GET'])
def get_inquiries():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id 필요'}), 400

    docs = list(inquiry_col.find({'user_id': user_id}))
    for doc in docs:
        doc['_id'] = str(doc['_id'])
        doc['created_at'] = doc['created_at'].strftime('%Y-%m-%d %H:%M:%S')
    return jsonify(docs)

# 탈퇴 시 탈퇴 사유 DB에 저장
@app.route('/insert_cancel_reason', methods=['POST'])
def insert_cancel_reason():
    data = request.get_json()
    user_id = data.get('user_id')
    reason = data.get('reason')
    date = data.get('date', datetime.now().strftime('%Y.%m.%d'))
    
    if not user_id or not reason:
        return jsonify({'error': 'user_id와 reason은 필수입니다.'}), 400

    doc = {
        'user_id': user_id,
        'reason': reason,
        'date': date,
        'created_at': datetime.now()
    }
    result = quit_reasons_col.insert_one(doc)   # ★ 여기서 사용!
    return jsonify({'result': 'success', '_id': str(result.inserted_id)}), 200

# 비밀번호 변경 
@app.route('/change_password', methods=['POST'])
@app.route('/change_password', methods=['POST'])
def change_password():
    data = request.json
    user_id = data.get('user_id')
    current_pw = data.get('current_password')
    new_pw = data.get('new_password')

    if not user_id or not current_pw or not new_pw:
        return jsonify({'error': '필수 정보 누락!'}), 400

    user = users.find_one({'_id': ObjectId(user_id)})
    if not user:
        return jsonify({'error': '사용자 없음'}), 404

    # hash 비교
    if not check_password_hash(user.get('password', ''), current_pw):
        return jsonify({'error': '현재 비밀번호가 올바르지 않습니다.'}), 401

    # 새 비밀번호 해시로 저장
    hashed_new_pw = generate_password_hash(new_pw)
    result = users.update_one({'_id': ObjectId(user_id)}, {'$set': {'password': hashed_new_pw}})
    if result.matched_count == 1:
        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({'error': '업데이트 실패'}), 500

# 키워드들 직접 받아오기
@app.route('/get_keywords')
def get_keywords():
    # 예: keywords 컬렉션에 {"keyword": "저당"} 이렇게 저장됨
    keywords = list(db.keywords.find({}, {'_id': 0, 'keyword': 1}))
    return jsonify([k['keyword'] for k in keywords])


# 실험실! DB 상 레시피 불러오기!
@app.route('/search_recipes')
def search_recipes():
    query = request.args.get('query', '').strip()
    order = request.args.get('order', 'latest')  # ⭐️ 추가! 기본값 최신순

    # 검색 조건
    search_filter = {
        "$or": [
            {"name": {"$regex": query, "$options": "i"}},
            {"keywords": {"$elemMatch": {"$regex": query, "$options": "i"}}},
            {"ingredients": {"$elemMatch": {"$regex": query, "$options": "i"}}},
        ]
    } if query else {}

    # 정렬 기준
    if order == 'views':
        sort_key = [('views', -1)]
    else:
        sort_key = [('_id', -1)]  # 최신순

    # _id는 빼고 전송 (원하면 포함 가능)
    cursor = db.recipes.find(search_filter).sort(sort_key)
    recipes = []
    for doc in cursor:
        doc['_id'] = str(doc['_id'])  # ObjectId를 string으로 변환
        recipes.append(doc)
    return jsonify(recipes)



# 실험실! DB 상 레시피 조회수 전달 !
@app.route('/increase_recipe_view', methods=['POST'])
def increase_recipe_view():
    recipe_id = request.json.get('id')
    if not recipe_id or not isinstance(recipe_id, str):
        return jsonify({'error': '레시피 id 없음 또는 형식 오류'}), 400

    # ObjectId 변환 체크
    try:
        obj_id = ObjectId(recipe_id)
    except (bson_errors.InvalidId, TypeError, ValueError):
        return jsonify({'error': '유효하지 않은 ObjectId'}), 400

    # 업데이트
    result = db.recipes.update_one({'_id': obj_id}, {'$inc': {'views': 1}})
    if result.matched_count == 1:
        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({'error': '레시피 찾지 못함'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
