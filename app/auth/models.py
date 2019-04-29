from app import db, login_manager
from app.posts.models import Post
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

# UserMixin: is_authenticated, is_active, is_anonymous, get_id

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    nickname = db.Column(db.String(20))
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    avatar = db.Column(db.String(20), nullable=False, default="default.jpg") # save only avatar image name
    posts = db.relationship('Post', backref='author', lazy=True) # here Post is a Model name. It creates 'author' column there

    def get_reset_token(self, expire_sec=30*60): # 30 minutes to reset the password
        s = Serializer(current_app.config['SECRET_KEY'], expire_sec)
        token = s.dumps({'user_id': self.id}).decode('utf-8')
        return token

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
