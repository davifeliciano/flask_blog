from flask import Blueprint, url_for, render_template, flash, redirect, request, abort
from flask_login import current_user, login_required
from .forms import PostForm, CommentForm
from ..models import Post, Comment
from flask_blog import db

posts = Blueprint("posts", __name__)


@posts.route("/post/new", methods=("GET", "POST"))
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data, content=form.content.data, author=current_user
        )
        db.session.add(post)
        db.session.commit()
        flash("Your post has been created!", "success")
        return redirect(url_for("main.homepage"))
    return render_template(
        "create_post.html", title="New Post", form=form, legend="New Post"
    )


@posts.route("/post/<int:post_id>", methods=("GET", "POST"))
def post(post_id):
    page = request.args.get("page", 1, type=int)
    post = Post.query.get_or_404(post_id)
    form = CommentForm()

    if form.validate_on_submit():
        comment = Comment(content=form.content.data, author=current_user, post=post)
        db.session.add(comment)
        db.session.commit()
        flash("Your comment has been posted!", "success")
        return redirect(url_for("posts.post", post_id=post.id))

    comments = (
        Comment.query.filter_by(post_id=post.id)
        .order_by(Comment.date_posted.asc())
        .paginate(per_page=5, page=page)
    )
    return render_template(
        "post.html", title=post.title, post=post, form=form, comments=comments
    )


@posts.route("/post/<int:post_id>/update", methods=("GET", "POST"))
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Your post has been updated!", "success")
        return redirect(url_for("posts.post", post_id=post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template(
        "create_post.html", title="New Post", form=form, legend="Update Post"
    )


@posts.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted!", "success")
    return redirect(url_for("main.homepage"))
