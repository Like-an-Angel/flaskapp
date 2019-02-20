from flask import Blueprint

auth = Blueprint('auth', __name__) # auth for name of the blueprint

from app.auth import routes
