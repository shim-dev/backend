from flask import Flask
from flask_cors import CORS

# 라우트 import
from routes.signup.auth_routes import auth_bp
from routes.signup.nick_routes import nick_bp
from routes.signup.birth_routes import birth_bp
from routes.signup.gender_routes import gender_bp
from routes.signup.height_routes import height_bp
from routes.signup.activity_routes import activity_bp
from routes.signup.sleep_routes import sleep_bp
from routes.signup.caffeine_routes import caffeine_bp
from routes.signup.alcohol_routes import alcohol_bp
from routes.mypage.mypage import mypage_bp
from routes.mypage.bookmark import bookmark_bp
from routes.mypage.notice import notice_bp
from routes.mypage.event import event_bp
from routes.mypage.faq import faq_bp
from routes.mypage.inquiry import inquiry_bp


app = Flask(__name__)
CORS(app)

# 블루프린트 등록
app.register_blueprint(auth_bp)
app.register_blueprint(nick_bp)
app.register_blueprint(birth_bp)
app.register_blueprint(gender_bp)
app.register_blueprint(height_bp)
app.register_blueprint(activity_bp)
app.register_blueprint(sleep_bp)
app.register_blueprint(caffeine_bp)
app.register_blueprint(alcohol_bp)
app.register_blueprint(mypage_bp)
app.register_blueprint(bookmark_bp)
app.register_blueprint(notice_bp)
app.register_blueprint(event_bp)
app.register_blueprint(faq_bp)
app.register_blueprint(inquiry_bp)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
