from flask import Blueprint, request, jsonify
from config import users  
from bson import ObjectId

nick_bp = Blueprint('nick', __name__)

@nick_bp.route('/set_nickname', methods=['POST'])
def set_nickname():
    data = request.json
    user_id = data.get('user_id')
    nickname = data.get('nickname')
    profile_url = data.get('profile_url')  

    if not user_id or not nickname:
        return jsonify({"message": "user_id와 닉네임이 필요합니다."}), 400

    # 닉네임 중복 확인
    if users.find_one({"nickname": nickname}):
        return jsonify({"message": "이미 사용 중인 닉네임입니다."}), 409

    try:
        object_id = ObjectId(user_id)
    except Exception:
        return jsonify({"message": "user_id 형식이 잘못되었습니다."}), 400

    #  저장할 필드 구성
    update_data = {"nickname": nickname}
    if profile_url:
        update_data["profile_url"] = profile_url

    result = users.update_one(
        {"_id": object_id},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        return jsonify({"message": "해당 user_id를 가진 사용자가 없습니다."}), 404

    return jsonify({"message": "닉네임 및 프로필 이미지 저장 성공!"}), 200