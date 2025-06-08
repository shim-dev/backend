from flask import Blueprint, request, jsonify
from datetime import datetime
from config import db
from bson import ObjectId
from bson.errors import InvalidId
from config import users
from werkzeug.security import check_password_hash, generate_password_hash

mypage_bp = Blueprint("mypage", __name__, url_prefix="/api/mypage")

@mypage_bp.route('/user', methods=['GET'])  
def get_user_info():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({ "message": "user_id 파라미터가 필요합니다." }), 400

    try:
        object_id = ObjectId(user_id)
        user = db.users.find_one({'_id': object_id})  

        if not user:
            return jsonify({ "message": "유저를 찾을 수 없습니다." }), 404

        return jsonify({
            'email': user.get('email'),
            'nickname': user.get('nickname'),
            'profile_url': user.get('profile_url'),
        }), 200

    except InvalidId:
        return jsonify({ "message": "유효하지 않은 user_id 형식입니다." }), 400

    except Exception as e:
        print("[ERROR] 서버 오류:", e)
        return jsonify({ "message": "서버 오류가 발생했습니다." }), 500

@mypage_bp.route('/nickname', methods=['POST'])
def update_nickname():
    data = request.get_json()
    user_id = data.get('user_id')
    nickname = data.get('nickname')

    if not user_id or not nickname:
        return jsonify({'error': '입력 오류'}), 400

    result = users.update_one({'_id': ObjectId(user_id)}, {'$set': {'nickname': nickname}})

    if result.modified_count == 1:
        return jsonify({'message': '닉네임 변경 성공'}), 200
    else:
        return jsonify({'message': '변경된 내용 없음 또는 유저 없음'}), 400

@mypage_bp.route('/change_password', methods=['POST'])
def change_password():
    data = request.get_json()
    user_id = data.get('user_id')
    current_pw = data.get('current_password')
    new_pw = data.get('new_password')

    user = users.find_one({'_id': ObjectId(user_id)})

    if not user:
        return jsonify({'error': '사용자 없음'}), 404

    if not check_password_hash(user['password'], current_pw):
        return jsonify({'error': '현재 비밀번호가 틀립니다.'}), 400  

    # 비밀번호 업데이트
    new_hash = generate_password_hash(new_pw)
    users.update_one({'_id': ObjectId(user_id)}, {'$set': {'password': new_hash}})
    return jsonify({'message': '비밀번호 변경 성공'}), 200

@mypage_bp.route('/health_profile', methods=['GET'])
def get_health_profile():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id 필요'}), 400

    profile = db.health_profiles.find_one({'user_id': user_id})
    if not profile:
        return jsonify({'error': '프로필 없음'}), 404

    return jsonify({
        'height': profile.get('height'),
        'weight': profile.get('weight'),
        'activity_level': profile.get('activity_level'),
        'sleep_hour': profile.get('sleep_hour'),
        'caffeine_cup': profile.get('caffeine_cup'),
        'alcohol_cup': profile.get('alcohol_cup'),
    }), 200

@mypage_bp.route('/withdrawal', methods=['POST'])
def withdrawal():
    data = request.get_json()
    user_id = data.get('user_id')
    reason = data.get('reason', '')

    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400

    try:
        object_id = ObjectId(user_id)  

        # 1. 탈퇴 사유 저장
        db.quit_reasons.insert_one({
            'user_id': object_id,
            'reason': reason,
            'timestamp': datetime.utcnow()
        })

        # 2. 관련 데이터 완전 삭제
        db.users.delete_one({'_id': object_id})
        db.health_profiles.delete_many({'user_id': object_id})
        db.bookmarks.delete_many({'user_id': object_id})
        db.records.delete_many({'user_id': object_id})
        db.sleep_hours.delete_many({'user_id': object_id})
        db.water_records.delete_many({'user_id': object_id})
        db.inquiries.delete_many({'user_id': object_id})
        db.images_col.delete_many({'user_id': object_id})  # 프로필 사진 등

        return jsonify({'message': '회원 탈퇴 완료'}), 200

    except Exception as e:
        print(f"❌ 회원 탈퇴 중 오류: {e}")
        return jsonify({'error': '서버 오류'}), 500