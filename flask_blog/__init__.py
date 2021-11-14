from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_manager
from flask_mail import Mail
from flask_moment import Moment
from .config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"
mail = Mail()
moment = Moment()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    moment.init_app(app)

    from .main.routes import main
    from .users.routes import users
    from .posts.routes import posts
    from .errors.handlers import errors

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(errors)

    from .models import User, Post

    @app.context_processor
    def inject_recent_posts():
        return dict(
            recent_posts=Post.query.order_by(Post.date_posted.desc()).limit(5).all()
        )

    @app.context_processor
    def inject_recent_users():
        return dict(
            recent_users=User.query.order_by(User.date_signed_in.desc()).limit(8).all()
        )

    return app
