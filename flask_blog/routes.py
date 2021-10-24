import os
import secrets
from PIL import Image
from flask import url_for, render_template, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from .forms import RegistrationForm, LoginForm, UpdateAccountForm
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


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + file_ext
    picture_path = os.path.join(app.root_path, "static/profile_pics", picture_filename)

    output_size = (125, 125)
    image = Image.open(form_picture)
    image.thumbnail(output_size)
    image.save(picture_path)
    return picture_filename


@app.route("/account", methods=("GET", "POST"))
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_filename = save_picture(form.picture.data)
            current_user.image_file = picture_filename
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated!", "success")
        return redirect(url_for("account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for("static", filename=f"profile_pics/{current_user.image_file}")
    return render_template(
        "account.html", title="Account", image_file=image_file, form=form
    )
