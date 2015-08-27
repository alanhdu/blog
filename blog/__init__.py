import datetime as dt

from flask import Flask, render_template, abort, redirect, url_for
import toolz

app = Flask(__name__)

def paginate(page, per_page=10):
    posts = app.config["BLOG"]["posts"]
    return posts[per_page * (page - 1): per_page * page]

@app.route("/", defaults={"page": 1})
@app.route("/<int:page>")
def index(page):
    posts = paginate(page)
    if not posts:
        abort(404)

    last_page = len(paginate(page + 1)) == 0

    return render_template("index.html", posts=posts, page=page,
                           last_page=last_page)

@app.route("/categories")
def categories():
    groups = toolz.groupby(lambda x: x.category,
                           app.config["BLOG"]["posts"])
    return render_template("categories.html", groups=groups)

def get_post(date: dt.date) -> "Optional[Post]":
    for p in app.config["BLOG"]["posts"]:
        if p.revdate == date:
            return p

@app.route("/post/<int:year>/<int:month>/<int:day>/")
def post(year, month, day):
    post = get_post(dt.date(year=year, month=month, day=day))
    if post is None:
        abort(404)

    return render_template("post.html", post=post)
