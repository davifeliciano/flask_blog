from datetime import datetime
from flask import Flask, url_for, render_template, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "0eb3217c80a4da9c5f2562a800c53d38"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db = SQLAlchemy(app)


# Creating database models
# Each class represents a table in the database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship("Post", backref="author", lazy=True)

    def __repr__(self) -> str:
        return f"User(username='{self.username}', email='{self.email}', image_file='{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self) -> str:
        return f"Post(title='{self.title}', date_posted='{self.date_posted}')"


# Test data
posts = [
    {
        "author": "Davi Feliciano",
        "title": "First Post!",
        "content": "This is the first post on the blog!",
        "date": "Epoch",
    },
    {
        "author": "Victor Rebeque",
        "title": "Second Post!",
        "content": "This is the second post on the blog!",
        "date": "Epoch Plus One",
    },
]


@app.route("/")
@app.route("/home")
def homepage():
    return render_template("homepage.html", posts=posts)


@app.route("/about")
def about():
    return render_template("about.html", title="About Us")


@app.route("/register", methods=("GET", "POST"))
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}!", "success")
        return redirect(url_for("homepage"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=("GET", "POST"))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "admin@blog.com" and form.password.data == "password":
            flash("You are now logged in!", "success")
            return redirect(url_for("homepage"))
        else:
            flash("Unsuccesful login. Please, check email and password.", "danger")
    return render_template("login.html", title="Login", form=form)


if __name__ == "__main__":
    app.run(debug=True)
