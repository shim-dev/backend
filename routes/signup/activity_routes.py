from flask import Blueprint, request, jsonify
from config import health_profiles
from bson import ObjectId

activity_bp = Blueprint('activity', __name__)

@activity_bp.route('/set_activity', methods=['POST'])
def set_activity():
    data = request.get_json()
    user_id = data.get('user_id')
    activity_level = data.get('activity_level')

    if not user_id or not activity_level:
        return jsonify({'success': False, 'message': 'user_id, 활동량 입력 필요'}), 400


    result = health_profiles.update_one(
        {'user_id': user_id},
        {'$set': {'activity_level': activity_level}},
        upsert=True
    )

    return jsonify({'success': True}), 200
