from flask import Blueprint, request, jsonify
from bson import ObjectId
from bson.errors import InvalidId
from datetime import datetime

from config import db

recipe_bp = Blueprint('recipe', __name__)

@recipe_bp.route('/get_keywords')
def get_keywords():
    # 예: keywords 컬렉션에 {"keyword": "저당"} 이렇게 저장됨
    keywords = list(db.keywords.find({}, {'_id': 0, 'keyword': 1}))
    return jsonify([k['keyword'] for k in keywords])


# 실험실! DB 상 레시피 불러오기!
@recipe_bp.route('/search_recipes')
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
@recipe_bp.route('/increase_recipe_view', methods=['POST'])
def increase_recipe_view():
    recipe_id = request.json.get('id')
    if not recipe_id or not isinstance(recipe_id, str):
        return jsonify({'error': '레시피 id 없음 또는 형식 오류'}), 400

    # ObjectId 변환 체크
    try:
        obj_id = ObjectId(recipe_id)
    except (InvalidId, TypeError, ValueError):
        return jsonify({'error': '유효하지 않은 ObjectId'}), 400

    # 업데이트
    result = db.recipes.update_one({'_id': obj_id}, {'$inc': {'views': 1}})
    if result.matched_count == 1:
        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({'error': '레시피 찾지 못함'}), 404
    
# 최근에 본 레시피 id 저장
@recipe_bp.route('/add_recent', methods=['POST'])
def add_recent():
    data = request.json

    # 1️⃣ 기존 중복 항목 제거
    db.recent_recipes.delete_many({
        "user_id": ObjectId(data["user_id"]),
        "recipe_id": ObjectId(data["recipe_id"])
    })

    db.recent_recipes.insert_one({
        "user_id": ObjectId(data["user_id"]),
        "recipe_id": ObjectId(data["recipe_id"]),
        "timestamp": datetime.utcnow()  # 최신순 정렬용
    })
    return jsonify(success=True)

# 최근에 본 레시피 불러오기
@recipe_bp.route('/get_recent')
def get_recent():
    user_id = request.args.get("user_id")
    recent_docs = db.recent_recipes.find(
        {"user_id": ObjectId(user_id)}
    ).sort("timestamp", -1).limit(10)

    recipe_ids = [doc["recipe_id"] for doc in recent_docs]
    recipes = list(db.recipes.find({"_id": {"$in": recipe_ids}}))

    for r in recipes:
        r["_id"] = str(r["_id"])
    return jsonify(recipes)

# 최근에 본 레시피 삭제하기
@recipe_bp.route('/delete_recent', methods=['DELETE'])
def delete_recent():
    user_id = request.args.get('user_id')
    recipe_id = request.args.get('recipe_id')
    db.recent_recipes.delete_one({
        "user_id": ObjectId(user_id),
        "recipe_id": ObjectId(recipe_id)
    })
    return jsonify(success=True)


# 북마크 추가하기
@recipe_bp.route('/bookmark_recipe', methods=['POST'])
def bookmark_recipe():
    data = request.json
    user_id = data.get('user_id')
    recipe_id = data.get('recipe_id')
    if not user_id or not recipe_id:
        return jsonify({'error': 'user_id와 recipe_id가 필요합니다.'}), 400

    # 이미 북마크했는지 체크(중복 방지)
    exists = db.bookmarks.find_one({
        'user_id': user_id,
        'recipe_id': recipe_id,
    })
    if exists:
        return jsonify({'status': 'already bookmarked'}), 200

    db.bookmarks.insert_one({
        'user_id': user_id,
        'recipe_id': recipe_id,
    })
    return jsonify({'status': 'bookmarked'})
