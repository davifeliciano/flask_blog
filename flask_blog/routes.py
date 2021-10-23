from flask import url_for, render_template, flash, redirect
from .forms import RegistrationForm, LoginForm
from .models import User, Post
from flask_blog import app

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
