from flask import render_template, request, redirect, url_for
import mistune

from blog import app
from .database import session
from .models import Post


@app.route("/post/add", methods=["POST"])
def add_post_post():
    post = Post(
        title=request.form["title"],
        content=mistune.markdown(request.form["content"]))
    session.add(post)
    session.commit()
    return redirect(url_for("posts"))


@app.route("/post/add", methods=["GET"])
def add_post_get():
    return render_template("add_post.html")


@app.route("/post/<int:pid>/edit", methods=["POST"])
def edit_post_post(pid):
    post = session.query(Post).get(pid)
    post.title = request.form["title"]
    post.content = mistune.markdown(request.form["content"])
    session.commit()
    return redirect(url_for("view_post", pid=pid))


@app.route("/post/<int:pid>/edit", methods=["GET"])
def edit_post_get(pid):
    post = session.query(Post).get(pid)
    return render_template("edit_post.html",
                           post=post)


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
                           has_prev=has_prev)


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
                           total_pages=total_pages)
