from flask import Blueprint, request, jsonify
from config import db
from bson import ObjectId
from bson.errors import InvalidId

mypage_bp = Blueprint("mypage", __name__, url_prefix="/api/mypage")

@mypage_bp.route('/user', methods=['GET'])  
def get_user():
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
            'profileImageUrl': user.get('profileImageUrl'),
            'notificationEnabled': user.get('notificationEnabled')
        }), 200

    except InvalidId:
        return jsonify({ "message": "유효하지 않은 user_id 형식입니다." }), 400

    except Exception as e:
        print("[ERROR] 서버 오류:", e)
        return jsonify({ "message": "서버 오류가 발생했습니다." }), 500


