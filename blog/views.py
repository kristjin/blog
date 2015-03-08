from flask import flash, render_template, request, redirect, url_for
from flask.ext.login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
import mistune

from blog import app
from .database import session
from .models import Post, User



@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("posts"))



@app.route("/login", methods=["POST"])
def login_post():
    email = request.form["email"]
    password = request.form["password"]
    user = session.query(User).filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash("Incorrect username or password", "danger")
        return redirect(url_for("login_get"))

    login_user(user)
    return redirect(request.args.get('next') or url_for("posts"))


@app.route("/login", methods=["GET"])
def login_get():
    return render_template("login.html")


@app.route("/post/add", methods=["POST"])
@login_required
def add_post_post():
    post = Post(
        title=request.form["title"],
        content=mistune.markdown(request.form["content"]),
        author=current_user
    )
    session.add(post)
    session.commit()
    return redirect(url_for("posts"))


@app.route("/post/add", methods=["GET"])
@login_required
def add_post_get():
    return render_template("add_post.html")


@app.route("/post/<int:pid>/edit", methods=["POST"])
@login_required
def edit_post_post(pid):
    post = session.query(Post).get(pid)
    post.title = request.form["title"]
    post.content = mistune.markdown(request.form["content"])
    session.commit()
    return redirect(url_for("view_post", pid=pid))


@app.route("/post/<int:pid>/edit", methods=["GET"])
@login_required
def edit_post_get(pid):
    post = session.query(Post).get(pid)
    return render_template("edit_post.html",
                           post=post,
                           current_user=current_user)


@app.route("/post/")
@app.route("/post/<int:pid>")
def view_post(pid=0):

    count = session.query(Post).count()

    has_next = pid < count - 1  # because it's a zer0 index
    has_prev = pid > 0

    post = session.query(Post).get(pid)

    return render_template("view_post.html",
                           pid=pid,
                           post=post,
                           has_next=has_next,
                           has_prev=has_prev,
                           current_user=current_user)


@app.route('/post/<int:pid>/delete', methods=["GET"])
@login_required
def delete_post_get(pid):
    post = session.query(Post).get(pid)
    return render_template("delete_post.html",
                           pid=pid,
                           post=post,
                           current_user=current_user)


@app.route('/post/<int:pid>/delete', methods=["POST"])
@login_required
def delete_post_post(pid):
    post = session.query(Post).get(pid)
    session.delete(post)
    session.commit()
    return redirect(url_for("posts"))


@app.route("/")
@app.route("/page/<int:page>")
def posts(page=1, paginate_by=10):
    # Zero-indexed page
    page_index = page - 1

    count = session.query(Post).count()

    start = page_index * paginate_by
    end = start + paginate_by

    total_pages = (count - 1) / paginate_by + 1
    has_next = page_index < total_pages - 1
    has_prev = page_index > 0

    posts = session.query(Post)
    posts = posts.order_by(Post.datetime.desc())
    posts = posts[start:end]

    return render_template("posts.html",
                           posts=posts,
                           has_next=has_next,
                           has_prev=has_prev,
                           page=page,
                           total_pages=total_pages,
                           current_user=current_user)
