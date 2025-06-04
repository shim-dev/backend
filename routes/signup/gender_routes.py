from flask import Blueprint, request, jsonify
from config import users
from bson import ObjectId

gender_bp = Blueprint('gender', __name__)

@gender_bp.route('/set_gender', methods=['POST'])
def set_gender():
    data = request.get_json()
    user_id = data.get('user_id')
    gender = data.get('gender')

    if not user_id or not gender:
        return jsonify({'success': False, 'message': 'user_id 또는 성별 누락'}), 400

    try:
        object_id = ObjectId(user_id)
    except Exception:
        return jsonify({'success': False, 'message': 'user_id 형식 오류'}), 400

    result = users.update_one({'_id': object_id}, {'$set': {'gender': gender}})
    if result.matched_count == 0:
        return jsonify({'success': False, 'message': '사용자를 찾을 수 없습니다.'}), 404

    return jsonify({'success': True}), 200
