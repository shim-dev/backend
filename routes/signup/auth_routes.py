from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from config import users
from bson import ObjectId

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')

        if users.find_one({"email": email}):
            return jsonify({"message": "이미 가입된 이메일입니다."}), 400

        hashed_pw = generate_password_hash(password)
        result = users.insert_one({
            "email": email,
            "password": hashed_pw,
            "created_at": datetime.utcnow()
        })

        return jsonify({
            "message": "회원가입 성공!",
            "user_id": str(result.inserted_id)
        }), 200

    except Exception as e:
        # 추후 로깅방식으로 변경 예정
        print('서버오류:', e)
        return jsonify({"message": "서버 오류가 발생했습니다."}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'success': False, 'message': '이메일 또는 비밀번호 누락'}), 400

    user = users.find_one({'email': email})
    if not user:
        return jsonify({'success': False, 'message': '가입된 이메일이 없습니다.'}), 401

    if not check_password_hash(user['password'], password):
        return jsonify({'success': False, 'message': '비밀번호가 일치하지 않습니다.'}), 401

    # 로그인 성공: user_id 반환
    return jsonify({
        'success': True,
        'user_id': str(user['_id']),
        'nickname': user.get('nickname', '')  # 닉네임 등 추가 반환 가능
    }), 200