import os


class Config:
    SECRET_KEY = os.environ.get("FLASK_BLOG_SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("FLASK_BLOG_SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get("FLASK_BLOG_MAIL_SERVER")
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_DEFAULT_SENDER = "noreply@flaskblogdemo.com"
    MAIL_USERNAME = os.environ.get("FLASK_BLOG_EMAIL_USER")
    MAIL_PASSWORD = os.environ.get("FLASK_BLOG_EMAIL_PWD")
