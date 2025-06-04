from flask import Blueprint, request, jsonify
from bson import ObjectId
from config import records, water_records, sleep_hours

record_bp = Blueprint('record', __name__)

# 음식 기록 등록
@record_bp.route('/insert_record', methods=['POST'])
def insert_record():
    data = request.json
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id 누락!'}), 400
    records.update_one(
        {
            'user_id': user_id,
            'date': data['date'],
            'mealType': data['mealType'],
            'name': data['name']
        },
        {'$set': data}, upsert=True
    )
    return jsonify({'status': 'success'})

# 음식 기록 받아오기
@record_bp.route('/get_records', methods=['GET'])
def get_records():
    user_id = request.args.get('user_id')
    date = request.args.get('date')
    mealType = request.args.get('mealType')
    if not user_id:
        return jsonify({'error': 'user_id 누락!'}), 400
    result = list(records.find({'user_id': user_id, 'date': date, 'mealType': mealType}))
    for doc in result:
        doc['_id'] = str(doc['_id'])
    return jsonify(result)

# 기록 삭제
@record_bp.route('/delete_record', methods=['DELETE'])
def delete_record():
    record_id = request.args.get('id')
    user_id = request.args.get('user_id')
    if not record_id or not user_id:
        return jsonify({'error': 'No id or user_id provided'}), 400
    try:
        result = records.delete_one({'_id': ObjectId(record_id), 'user_id': user_id})
        if result.deleted_count == 1:
            return jsonify({'status': 'deleted'})
        else:
            return jsonify({'error': 'Record not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
# 기록 수정
@record_bp.route('/update_record', methods=['PUT'])
def update_record():
    data = request.json
    record_id = data.get('_id')
    user_id = data.get('user_id')
    if not record_id or not user_id:
        return jsonify({'error': 'No _id or user_id provided'}), 400
    update_data = {k: v for k, v in data.items() if k != '_id'}
    try:
        result = records.update_one(
            {'_id': ObjectId(record_id), 'user_id': user_id},
            {'$set': update_data}
        )
        if result.matched_count == 1:
            return jsonify({'status': 'updated'})
        else:
            return jsonify({'error': 'Record not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 모든 기록 받아오기 
@record_bp.route('/get_all_records')
def get_all_records():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id 누락!'}), 400
    records_list = list(records.find({'user_id': user_id}))
    for r in records_list:
        r['_id'] = str(r['_id'])
    return jsonify(records_list)

# 물 저장
@record_bp.route('/save_water', methods=['POST'])
def save_water():
    data = request.json
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id 누락!'}), 400
    water_records.update_one(
        {'user_id': user_id, 'date': data['date']},
        {'$set': {'cups': data['cups']}},
        upsert=True
    )
    return jsonify({'status': 'success'})

# 물 기록 불러오기
@record_bp.route('/get_water', methods=['GET'])
def get_water():
    user_id = request.args.get('user_id')
    date = request.args.get('date')
    if not user_id:
        return jsonify({'error': 'user_id 누락!'}), 400
    result = water_records.find_one({'user_id': user_id, 'date': date}, {'_id': 0})
    return jsonify(result if result else {'cups': 0})

# 수면 기록 저장
@record_bp.route('/insert_or_update_sleep', methods=['POST'])
def insert_or_update_sleep():
    data = request.json
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({'error': 'user_id 누락!'}), 400
    sleep_hours.update_one(
        {'user_id': user_id, 'date': data['date']},
        {'$set': {'hours': data['hours']}},
        upsert=True
    )
    return jsonify({'status': 'success'})

# 수면 기록 받아오기
@record_bp.route('/get_sleep', methods=['GET'])
def get_sleep():
    user_id = request.args.get('user_id')
    date = request.args.get('date')
    if not user_id:
        return jsonify({'error': 'user_id 누락!'}), 400
    result = sleep_hours.find_one({'user_id': user_id, 'date': date}, {'_id': 0})
    return jsonify(result if result else {'hours': 0})
