from flask import Blueprint, url_for, render_template, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from .forms import (
    RegistrationForm,
    LoginForm,
    UpdateAccountForm,
    RequestResetForm,
    ResetPasswordForm,
)
from ..models import User, Post
from flask_blog import db, bcrypt
from .utils import save_picture, send_reset_email

users = Blueprint("users", __name__)


@users.route("/register", methods=("GET", "POST"))
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.homepage"))
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
        return redirect(url_for("users.login"))
    return render_template("register.html", title="Register", form=form)


@users.route("/login", methods=("GET", "POST"))
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.homepage"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            flash("You are now logged in!", "success")
            return (
                redirect(next_page) if next_page else redirect(url_for("main.homepage"))
            )
        else:
            flash("Unsuccesful login. Please, check email and password.", "danger")
    return render_template("login.html", title="Login", form=form)


@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.homepage"))


@users.route("/account", methods=("GET", "POST"))
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
        return redirect(url_for("users.account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for("static", filename=f"profile_pics/{current_user.image_file}")
    return render_template(
        "account.html", title="Account", image_file=image_file, form=form
    )


@users.route("/user/<username>")
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get("page", 1, type=int)
    posts = (
        Post.query.order_by(Post.date_posted.desc())
        .filter_by(author=user)
        .paginate(per_page=5, page=page)
    )
    return render_template("user.html", title=user.username, user=user, posts=posts)


@users.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("main.homepage"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_email(user)
            flash(
                "An email has been sent to your address with instructions to reset your password.",
                "info",
            )
            return redirect(url_for("users.login"))
    return render_template("reset_request.html", title="Reset Password", form=form)


@users.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.homepage"))
    user = User.verify_reset_token(token)
    if not user:
        return redirect(url_for("users.reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        db.session.commit()
        flash("Your password has been updated! You are now able to login.", "success")
        return redirect(url_for("users.login"))
    return render_template("reset_token.html", title="Reset Password", form=form)
