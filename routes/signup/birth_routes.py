from flask import Blueprint, request, jsonify
from config import users  
from bson import ObjectId

birth_bp = Blueprint('birth', __name__)

@birth_bp.route('/set_birth', methods=['POST'])
def set_birth():
    data = request.get_json()
    user_id = data.get('user_id')
    birth = data.get('birth')

    if not user_id or not birth:
        return jsonify({'success': False, 'message': 'user_id 또는 생년월일 누락'}), 400


    try:
        object_id = ObjectId(user_id)
    except Exception:
        return jsonify({'success': False, 'message': 'user_id 형식 오류'}), 400

    user = users.find_one({'_id': object_id})
    if not user:
        return jsonify({'success': False, 'message': '사용자 없음'}), 404

    users.update_one({'_id': object_id}, {'$set': {'birth': birth}})
    return jsonify({'success': True}),200
