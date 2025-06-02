from flask import Blueprint, jsonify
from config import db
from bson import ObjectId
from bson.errors import InvalidId

notice_bp = Blueprint("notice", __name__, url_prefix="/api/mypage")

@notice_bp.route('/notice', methods=['GET'])
def get_notices():
    try:
        notices_cursor = db.notices.find().sort('date', -1)  # 최신순 정렬
        notices = []
        for notice in notices_cursor:
            notices.append({
                "id": str(notice['_id']),
                "title": notice['title'],
                "date": notice['date'][:10]  # yyyy-mm-dd
            })
        return jsonify(notices), 200
    except Exception as e:
        print("❌ 공지사항 조회 오류:", e)
        return jsonify({"message": "서버 오류"}), 500


@notice_bp.route('/notice/<notice_id>', methods=['GET'])
def get_notice_detail(notice_id):
    try:
        notice = db.notices.find_one({"_id": ObjectId(notice_id)})
        if not notice:
            print("❌ 해당 ID로 공지사항 없음")
            return jsonify({"message": "공지사항을 찾을 수 없습니다."}), 404

        return jsonify({
            "id": str(notice['_id']),
            "title": notice['title'],
            "content": notice['content'],
            "date": notice['date'][:10]
        }), 200

    except InvalidId:
        print("❌ 잘못된 ObjectId 형식:", notice_id)
        return jsonify({"message": "잘못된 ID 형식입니다."}), 400

    except Exception as e:
        print("❌ 공지사항 상세 오류:", e)
        return jsonify({"message": "서버 오류"}), 500
