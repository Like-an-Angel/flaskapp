from app.posts import posts
from flask import render_template, redirect, url_for, flash, request
from app.posts.forms import PostingForm#, EditPostButton, DeletePostButton
from app import db
from flask_login import login_required, current_user
from app.posts.models import Post

@posts.route("/", methods=["GET", "POST"])
def home():
    try:
        allPosts = Post.query.order_by(Post.id).all()[::-1]
    except:
        allPosts = None

    # flash(f"We have {len(allPosts)} posts!", "info")
    return render_template("home.html", allPosts=allPosts)
    # return render_template("home.html")

@posts.route("/about")
def about():
    return render_template("about.html")

@posts.route("/post-editor", methods=["GET", "POST"])
@login_required
def post_editor():
    form = PostingForm()
    if form.validate_on_submit():
        title = form.title.data
        subtitle = form.subtitle.data
        content = form.content.data

        new_post = Post(title=title, subtitle=subtitle, content=content, user_id=current_user.id)

        db.session.add(new_post)
        db.session.commit()

        flash("Post has been created", "success")
        return redirect(url_for("posts.home"))
    return render_template("post_editor.html", form=form, post=None)

@posts.route("/post-editor/<id>", methods=["GET", "POST"])
@login_required
def post_editor_reedit(id):
    try:
        post = Post.query.filter_by(id=id).first()
    except:
        flash("There was an error loading the post", "warning")
        return redirect(url_for("posts.home"))
    if not post:
        flash("Post you are trying to edit doesn't exist", "warning")
        return redirect(url_for("posts.home"))
    form = PostingForm()
    if post.author.id != current_user.id:
        flash("You are not the owner of the post", "warning")
        return redirect(url_for("posts.home"))
    if request.method=="GET":
        form.title.data = post.title
        form.subtitle.data = post.subtitle
        form.content.data = post.content
    if form.validate_on_submit():
        post.title = form.title.data
        post.subtitle = form.subtitle.data
        post.content = form.content.data

        db.session.commit()

        flash("Post has been edited", "success")
        return redirect(url_for("posts.home"))
    return render_template("post_editor.html", form=form, post=None)

@posts.route("/post-delete/<id>", methods=["GET", "POST"])
@login_required
def post_delete(id):
    try:
        post = Post.query.filter_by(id=id).first()
    except:
        flash("There was an error accessing the post", "warning")
        return redirect(url_for("posts.home"))
    if not post:
        flash("Post you are trying to delete doesn't exist", "warning")
        return redirect(url_for("posts.home"))
    if post.author.id != current_user.id:
        flash("You are not the owner of the post", "warning")
        return redirect(url_for("posts.home"))
    db.session.delete(post)
    db.session.commit()
    flash("Post has been deleted", "success")
    return redirect(url_for("posts.home"))
