import os

SECRET_KEY = os.environ.get("SECRET_KEY")
SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(os.getcwd(),"flaskapp.db")}'
SQLALCHEMY_TRACK_MODIFICATIONS = False
DEBUG = True

MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = '587'
MAIL_USE_TLS = True

MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
