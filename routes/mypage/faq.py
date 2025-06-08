from flask import Blueprint, jsonify
from config import db  # MongoDB 연결
from bson import ObjectId

faq_bp = Blueprint("faq", __name__, url_prefix="/api/mypage")

@faq_bp.route("/faq", methods=["GET"])
def get_faq_list():
    try:
        faqs_cursor = db.faq.find()  # 'faqs' 컬렉션
        faqs = []

        for faq in faqs_cursor:
            faqs.append({
                "id": str(faq["_id"]),
                "question": faq["question"],
                "answer": faq["answer"]
            })

        return jsonify(faqs), 200

    except Exception as e:
        print("❌ FAQ 조회 오류:", e)
        return jsonify({"message": "서버 오류 발생"}), 500
