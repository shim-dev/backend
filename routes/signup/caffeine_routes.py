from flask import Blueprint, request, jsonify
from config import health_profiles
from bson import ObjectId

caffeine_bp = Blueprint('caffeine', __name__)

@caffeine_bp.route('/set_caffeine', methods=['POST'])
def set_caffeine():
    data = request.get_json()
    user_id = data.get('user_id')
    caffeine_cup = data.get('caffeine_cup')

    if not user_id or caffeine_cup is None:
        return jsonify({'success': False, 'message': 'user_id와 caffeine_cup 모두 필요합니다.'}), 400

    try:
        object_id = ObjectId(user_id)
    except Exception:
        return jsonify({'success': False, 'message': 'user_id 형식 오류'}), 400

    result = health_profiles.update_one(
        {'user_id': user_id},
        {'$set': {'caffeine_cup': caffeine_cup}},
        upsert=True
    )
    return jsonify({'success': True}), 200
