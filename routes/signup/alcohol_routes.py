
from flask import Blueprint, request, jsonify
from config import health_profiles
from bson import ObjectId

alcohol_bp = Blueprint('alcohol_cup', __name__)

@alcohol_bp.route('/set_alcohol', methods=['POST'])
def set_alcohol():
    data = request.get_json()
    user_id = data.get('user_id')
    alcohol_cup = data.get('alcohol_cup')

    if not user_id or alcohol_cup is None:
        return jsonify({'success': False, 'message': 'user_id 또는 알코올 섭취량 누락'}), 400

    try:
        object_id = ObjectId(user_id)
    except Exception:
        return jsonify({'success': False, 'message': 'user_id 형식 오류'}), 400

    result = health_profiles.update_one(
        {'user_id': user_id},
        {'$set': {'alcohol_cup': alcohol_cup}},
        upsert=True
    )
    return jsonify({'success': True}), 200
