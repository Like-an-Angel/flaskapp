# python
# import secrets
# secrets.token_hex(16) <- generates a key string
# app.config["SECRET_KEY"] = '23c3f0c3963ae910e959ab6a4ae6ce46' # can be any string
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flaskapp.db" # For sqlite has to be .db
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
import os

# SECRET_KEY = '23c3f0c3963ae910e959ab6a4ae6ce46'
SECRET_KEY = os.environ.get("SECRET_KEY")
SQLALCHEMY_DATABASE_URI = "sqlite:///flaskapp.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False
DEBUG = True
