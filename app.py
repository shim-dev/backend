from flask import Flask
from flask_cors import CORS

# 라우트 import
from routes.mypage.mypage import mypage_bp
from routes.mypage.bookmark import bookmark_bp
from routes.mypage.notice import notice_bp


app = Flask(__name__)
CORS(app)

# 블루프린트 등록
app.register_blueprint(mypage_bp)
app.register_blueprint(bookmark_bp)
app.register_blueprint(notice_bp)


# 채림 언니 파트 #
app.register_blueprint(auth_bp)
app.register_blueprint(nick_bp)
app.register_blueprint(birth_bp)
app.register_blueprint(gender_bp)
app.register_blueprint(height_bp)
app.register_blueprint(activity_bp)
app.register_blueprint(sleep_bp)
app.register_blueprint(caffeine_bp)
app.register_blueprint(alcohol_bp)
# 채림 언니 파트 끝 #

# 수아 언니 파트 #
app.register_blueprint(mypage_bp)
app.register_blueprint(bookmark_bp)
app.register_blueprint(notice_bp)
app.register_blueprint(event_bp)
app.register_blueprint(faq_bp)
app.register_blueprint(inquiry_bp)
# 수아 언니 파트 끝 #

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)