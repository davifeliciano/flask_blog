from flask import Blueprint, render_template, request
from ..models import Post

main = Blueprint("main", __name__)


@main.route("/")
@main.route("/home")
def homepage():
    page = request.args.get("page", 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=5, page=page)
    return render_template("homepage.html", title="Homepage", posts=posts)


@main.route("/about")
def about():
    return render_template("about.html", title="About")
