from flask import Blueprint, jsonify
from config import db
from bson import ObjectId
from bson.errors import InvalidId

event_bp = Blueprint("event", __name__, url_prefix="/api/mypage")

@event_bp.route("/event", methods=["GET"])
def get_events():
    try:
        events_cursor = db.events.find().sort("date", -1)  # 최신순
        events = []

        for event in events_cursor:
            events.append({
                "id": str(event["_id"]),
                "title": event["title"],
                "date": event["date"][:10],  # YYYY-MM-DD
            })

        return jsonify(events), 200

    except Exception as e:
        print("❌ 이벤트 목록 조회 오류:", e)
        return jsonify({"message": "서버 오류"}), 500

@event_bp.route('/event/<event_id>', methods=['GET'])
def get_event_detail(event_id):
    try:
        event = db.events.find_one({'_id': ObjectId(event_id)})
        if not event:
            return jsonify({'message': '해당 이벤트를 찾을 수 없습니다.'}), 404

        return jsonify({
            'id': str(event['_id']),
            'title': event['title'],
            'date': event['date'],
            'content': event['content'],
        }), 200

    except InvalidId:
        return jsonify({'message': '유효하지 않은 ID입니다.'}), 400
    except Exception as e:
        print("❌ 이벤트 상세 조회 오류:", e)
        return jsonify({'message': '서버 오류가 발생했습니다.'}), 500