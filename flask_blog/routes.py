from flask import url_for, render_template, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from .forms import RegistrationForm, LoginForm
from .models import User, Post
from flask_blog import app, db, bcrypt

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
    return render_template("homepage.html", title="Homepage", posts=posts)


@app.route("/about")
def about():
    return render_template("about.html", title="About")


@app.route("/register", methods=("GET", "POST"))
def register():
    if current_user.is_authenticated:
        return redirect(url_for("homepage"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
        )
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created!", "success")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=("GET", "POST"))
def login():
    if current_user.is_authenticated:
        return redirect(url_for("homepage"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            flash("You are now logged in!", "success")
            return redirect(next_page) if next_page else redirect(url_for("homepage"))
        else:
            flash("Unsuccesful login. Please, check email and password.", "danger")
    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("homepage"))


@app.route("/account")
@login_required
def account():
    return render_template("account.html", title="Account")
