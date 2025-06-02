from flask import Blueprint, request, jsonify
from config import health_profiles

sleep_bp = Blueprint('sleep', __name__)

@sleep_bp.route('/set_sleep', methods=['POST'])
def set_sleep():
    data = request.get_json()
    user_id = data.get('user_id')
    sleep_hour = data.get('sleep_hour')

    if not user_id or sleep_hour is None:
        return jsonify({'success': False, 'message': 'user_id, 수면시간 입력 필요'}), 400

    result = health_profiles.update_one(
        {'user_id': user_id},
        {'$set': {'sleep_hour': sleep_hour}},
        upsert=True
    )
    return jsonify({'success': True}), 200
