from flask import Blueprint, jsonify

records_bp = Blueprint('records', __name__)

@records_bp.route('/ping', methods=['GET'])
def ping():
    return jsonify({'message': 'pong'}), 200
