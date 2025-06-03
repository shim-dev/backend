from flask import Flask
from flask_cors import CORS
from routes.signup.auth_routes import auth_bp
from routes.signup.nick_routes import nick_bp
from routes.signup.birth_routes import birth_bp
from routes.signup.gender_routes import gender_bp
from routes.signup.height_routes import height_bp
from routes.signup.activity_routes import activity_bp
from routes.signup.sleep_routes import sleep_bp
from routes.signup.caffeine_routes import caffeine_bp
from routes.signup.alcohol_routes import alcohol_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(auth_bp)
app.register_blueprint(nick_bp)
app.register_blueprint(birth_bp)
app.register_blueprint(gender_bp)
app.register_blueprint(height_bp)
app.register_blueprint(activity_bp)
app.register_blueprint(sleep_bp)
app.register_blueprint(caffeine_bp)
app.register_blueprint(alcohol_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
