import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize extensions
jwt = JWTManager()
db = SQLAlchemy()
migrate = Migrate()

UPLOAD_FOLDER = 'uploads'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(APP_ROOT)
ABSOLUTE_UPLOAD_FOLDER = os.path.join(PROJECT_ROOT, UPLOAD_FOLDER)

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "longphan-secure-secret-key"
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    jwt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    from app.controllers.auth import auth_bp
    from app.controllers.user import user_bp
    from app.controllers.upload import upload_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/user')
    app.register_blueprint(upload_bp, url_prefix='/api/upload')

    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(ABSOLUTE_UPLOAD_FOLDER, filename)

    if not os.path.exists(ABSOLUTE_UPLOAD_FOLDER):
        os.makedirs(ABSOLUTE_UPLOAD_FOLDER)

    return app
