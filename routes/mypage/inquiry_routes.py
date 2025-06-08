from flask import Blueprint, request, jsonify
from config import db
from bson import ObjectId
from datetime import datetime
from config import inquiry_col

inquiry_bp = Blueprint("inquiry", __name__, url_prefix="/api/mypage")

@inquiry_bp.route('/inquiries', methods=['GET'])
def get_inquiry_list():
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({'message': 'user_id가 필요합니다'}), 400

        inquiries = db.inquiries.find({'user_id': user_id}).sort('created_at', -1)

        result = []
        for inquiry in inquiries:
            result.append({
                'id': str(inquiry['_id']),
                'title': inquiry.get('title', ''),
                'content': inquiry.get('content', ''),
                'status': inquiry.get('status', '답변대기'),
                'created_at': str(inquiry.get('created_at', ''))[:10],
                'answer': inquiry.get('answer', ''),  # 문자열로 처리
                'answered_at': str(inquiry.get('responded_at', ''))[:10] if inquiry.get('responded_at') else None,
                'images': inquiry.get('images', [])  # 👈 이미지 리스트 포함
            })

        return jsonify(result), 200
    except Exception as e:
        print("❌ 1:1 문의 목록 조회 실패:", e)
        return jsonify({'message': '서버 오류'}), 500

@inquiry_bp.route('/inquiries', methods=['POST'])
def post_inquiry():
    data = request.get_json()

    inquiry_doc = {
        "user_id": data.get("user_id"),
        "title": data.get("title"),
        "content": data.get("content"),
        "status": "접수 중",
        "created_at": datetime.utcnow(),
        "images": [],
        "answer": "",
        "answered_at": None,
    }

    result = inquiry_col.insert_one(inquiry_doc) 
    return jsonify({"success": True, "inquiry_id": str(result.inserted_id)}), 200



