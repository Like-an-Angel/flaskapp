from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

db = SQLAlchemy() # Here, we don't have app yet
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message_category = "warning"

def create_app(config_type):
    app = Flask(__name__)

    configuration = os.path.join(os.getcwd(), "config", config_type+".py")
    app.config.from_pyfile(configuration)

    db.init_app(app) # attaching db to app
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from app.auth import auth
    from app.posts import posts

    app.register_blueprint(auth)
    app.register_blueprint(posts)

    return app

    # in python interpreter:
    # import secrets
    # secrets.token_hex(16) <- generates a key string
    # app.config["SECRET_KEY"] = '23c3f0c3963ae910e959ab6a4ae6ce46' # can be any string
    # app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flaskapp.db" # For sqlite has to be .db
    # app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
