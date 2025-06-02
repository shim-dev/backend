from flask import Flask
from flask_cors import CORS

# 라우트 import
from routes.mypage.mypage import mypage_bp
from routes.mypage.bookmark import bookmark_bp
from routes.mypage.notice import notice_bp
from routes.mypage.event import event_bp


app = Flask(__name__)
CORS(app)

# 블루프린트 등록
app.register_blueprint(mypage_bp)
app.register_blueprint(bookmark_bp)
app.register_blueprint(notice_bp)
app.register_blueprint(event_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
