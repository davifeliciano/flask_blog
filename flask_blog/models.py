from datetime import datetime, timedelta
import jwt
from flask import flash
from flask_blog import db, login_manager, app
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id: int):
    return User.query.get(int(user_id))


# Creating database models
# Each class represents a table in the database
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship("Post", backref="author", lazy=True)

    def __repr__(self) -> str:
        return f"User(username='{self.username}', email='{self.email}', image_file='{self.image_file}')"

    def get_reset_token(self, expires=30):
        delta = timedelta(minutes=expires)
        now = datetime.utcnow()
        exp_time = now + delta
        payload = {"exp": exp_time, "user_id": self.id}
        return jwt.encode(payload=payload, key=app.config["SECRET_KEY"])

    @staticmethod
    def verify_reset_token(token):
        try:
            user_id = jwt.decode(
                token,
                key=app.config["SECRET_KEY"],
                algorithms="HS256",
                leeway=120,
            )["user_id"]
        except jwt.ExpiredSignatureError:
            flash(
                "This token has expired. Please, make another reset request.", "warning"
            )
            return None
        except jwt.InvalidTokenError:
            flash("This is an invalid token. Plese, make a reset request.", "warning")
            return None
        return User.query.get(user_id)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self) -> str:
        return f"Post(title='{self.title}', date_posted='{self.date_posted}')"
