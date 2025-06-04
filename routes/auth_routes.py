from werkzeug.security import check_password_hash, generate_password_hash
from flask import Blueprint, request, jsonify
from config import users

auth_bp = Blueprint('auth', __name__)

# 로그인
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = users.find_one({'email': email})
    if user and check_password_hash(user['password'], password):  # hash 비교!
        return jsonify({
            'user_id': str(user['_id']),
            'nickname': user.get('nickname', ''),
            'email': user.get('email', '')
        }), 200
    else:
        return jsonify({'error': '이메일 또는 비밀번호가 올바르지 않습니다.'}), 401
    
# 회원가입
@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json
    email = data.get('email')
    nickname = data.get('nickname')
    password = data.get('password')

    if users.find_one({'email': email}):
        return jsonify({'error': '이미 존재하는 이메일입니다.'}), 400

    hashed_pw = generate_password_hash(password)  # 해시로 변환!
    result = users.insert_one({
        'email': email,
        'nickname': nickname,
        'password': hashed_pw,
    })
    return jsonify({'message': '회원가입 성공!', 'user_id': str(result.inserted_id), 'nickname': nickname, 'email' : email}), 200