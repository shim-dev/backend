from flask import Blueprint, request, jsonify
from config import health_profiles
from bson import ObjectId

height_bp = Blueprint('height', __name__)

@height_bp.route('/set_height_weight', methods=['POST'])
def set_height_weight():
    data = request.get_json()
    user_id = data.get('user_id')
    height = data.get('height')
    weight = data.get('weight')

    if not user_id or height is None or weight is None:
        return jsonify({'success': False, 'message': 'user_id, 키, 몸무게 모두 필요합니다.'}), 400

    try:
        object_id = ObjectId(user_id)
    except Exception:
        return jsonify({'success': False, 'message': 'user_id 형식 오류'}), 400

    # 이미 기록 있으면 업데이트, 없으면 삽입 
    result = health_profiles.update_one(
        {'user_id': user_id},
        {'$set': {'height': height, 'weight': weight}},
        upsert=True
    )
    return jsonify({'success': True}), 200
