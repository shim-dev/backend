from flask import Flask
from flask_cors import CORS
# routes에서 Blueprint import

from routes.mypage.mypage import mypage_bp
from routes.mypage.bookmark import bookmark_bp
from routes.mypage.notice import notice_bp
from routes.mypage.event import event_bp
from routes.mypage.faq import faq_bp
from routes.mypage.inquiry import inquiry_bp
from routes.auth_routes import auth_bp
from routes.record_routes import record_bp
#from routes.user_routes import user_bp
#from routes.yolo_routes import image_bp
#from routes.recipe_routes import recipe_bp
from routes.yolo_routes import yolo_bp

app = Flask(__name__)
CORS(app)

# Blueprint 등록
app.register_blueprint(mypage_bp)
app.register_blueprint(bookmark_bp)
app.register_blueprint(notice_bp)
app.register_blueprint(event_bp)
app.register_blueprint(faq_bp)
app.register_blueprint(inquiry_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(record_bp)
#app.register_blueprint(user_bp)
#app.register_blueprint(image_bp)
#app.register_blueprint(recipe_bp)
app.register_blueprint(yolo_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

