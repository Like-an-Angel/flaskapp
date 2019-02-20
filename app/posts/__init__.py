from flask import Blueprint

posts = Blueprint('posts', __name__) # auth for name of the blueprint

from app.posts import routes
