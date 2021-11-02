import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_manager
from flask_mail import Mail

app = Flask(__name__)
app.config["SECRET_KEY"] = "0eb3217c80a4da9c5f2562a800c53d38"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_DEFAULT_SENDER"] = "noreply@flaskblogdemo.com"
app.config["MAIL_USERNAME"] = os.environ.get("FLASK_BLOG_EMAIL_USER")
app.config["MAIL_PASSWORD"] = os.environ.get("FLASK_BLOG_EMAIL_PWD")
mail = Mail(app)

from flask_blog import routes
