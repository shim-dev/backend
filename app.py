from flask import Flask
from flask_cors import CORS

# routes에서 Blueprint import
from routes.record.record_routes import record_bp
#from routes.user_routes import user_bp
#from routes.yolo_routes import image_bp
from routes.recipe.recipe_routes import recipe_bp
from routes.yolo.yolo_routes import yolo_bp



# 채림 언니 파트 #
from routes.signup.auth_routes import auth_bp
from routes.signup.nick_routes import nick_bp
from routes.signup.birth_routes import birth_bp
from routes.signup.gender_routes import gender_bp
from routes.signup.height_routes import height_bp
from routes.signup.activity_routes import activity_bp
from routes.signup.sleep_routes import sleep_bp
from routes.signup.caffeine_routes import caffeine_bp
from routes.signup.alcohol_routes import alcohol_bp
# 채림 언니 파트 끝 #

app = Flask(__name__)
CORS(app)

# Blueprint 등록
app.register_blueprint(record_bp)
#app.register_blueprint(user_bp)
#app.register_blueprint(image_bp)
app.register_blueprint(recipe_bp)
app.register_blueprint(yolo_bp)


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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
