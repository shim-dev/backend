from flask import Blueprint, request, jsonify
from config import db
from bson import ObjectId
from bson.errors import InvalidId

bookmark_bp = Blueprint("bookmark", __name__, url_prefix="/api/mypage")

@bookmark_bp.route('/bookmark', methods=['GET'])
def get_bookmarked_recipes():
    user_id = request.args.get('user_id')
    page = int(request.args.get('page', 1))
    size = int(request.args.get('size', 10))

    if not user_id:
        return jsonify({"message": "user_id 파라미터가 필요합니다."}), 400

    try:
        # 유저 찾기
        object_id = ObjectId(user_id)
        user = db.users.find_one({"_id": object_id})
        if not user:
            return jsonify({"message": "유저를 찾을 수 없습니다."}), 404

        bookmark_ids = user.get("bookmarks", [])
        total = len(bookmark_ids)

        # 페이지네이션 적용
        start = (page - 1) * size
        end = start + size
        selected_ids = bookmark_ids[start:end]

        # 레시피 조회
        recipes_cursor = db.recipes.find({"recipeId": {"$in": selected_ids}})
        recipes = []
        for r in recipes_cursor:
            recipes.append({
                "recipeId": r.get("recipeId"),
                "title": r.get("name"),
                "description": r.get("desc"),
                "imageUrl": r.get("imageUrl"),
                "tags": r.get("keywords", []),
                "timeRequired": f"{r.get('time')}분",
                "difficulty": r.get("level"),
                "serving": f"{r.get('serving')}인분"
            })

        return jsonify({
            "total": total,
            "page": page,
            "size": size,
            "recipes": recipes
        }), 200

    except InvalidId:
        return jsonify({"message": "유효하지 않은 user_id입니다."}), 400
    except Exception as e:
        print("[ERROR] 북마크 조회 중 오류:", e)
        return jsonify({"message": "서버 오류가 발생했습니다."}), 500

@bookmark_bp.route('/bookmark', methods=['DELETE'])
def delete_bookmark():
    user_id = request.args.get('user_id')
    recipe_id = int(request.args.get('recipe_id', -1))

    if not user_id or recipe_id < 0:
        return jsonify({"message": "user_id와 recipe_id가 필요합니다."}), 400

    result = db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$pull": {"bookmarks": recipe_id}}
    )

    if result.modified_count:
        return jsonify({"message": "삭제 성공"}), 200
    else:
        return jsonify({"message": "이미 삭제되었거나 존재하지 않습니다."}), 404