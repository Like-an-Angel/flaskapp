from app import db, login_manager
from app.posts.models import Post
from flask_login import UserMixin

# UserMixin: is_authenticated, is_active, is_anonymous, get_id

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    avatar = db.Column(db.String(20), nullable=False, default="default.jpg") # We save only avatar image name
    posts = db.relationship('Post', backref='author', lazy=True) # here Post is a Model name. It creates 'author' column there.

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
