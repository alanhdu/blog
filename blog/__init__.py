import datetime as dt
import math
from urllib.parse import urljoin

from flask import Flask, render_template, abort, request, url_for
from werkzeug.contrib.atom import AtomFeed
import toolz

app = Flask(__name__)

def paginate(page):
    posts = app.config["BLOG"]["posts"]
    per_page = app.config["PER_PAGE"]
    return posts[per_page * (page - 1): per_page * page]

@app.route("/", defaults={"page": 1})
@app.route("/<int:page>.html")
def index(page, per_page=10):
    posts = app.config["BLOG"]["posts"]
    this_page = posts[per_page * (page - 1): per_page * page]

    if not this_page or page < 1:
        abort(404)

    num_pages = math.ceil(len(posts) / per_page)

    return render_template("index.html", posts=this_page, page=page,
                           num_pages=num_pages)

@app.route("/categories.html")
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

@app.route("/feed.atom")
def atom_feed():
    feed = AtomFeed(app.config["BLOG"]["site_title"],
                    feed_url=request.url, url=app.config["BLOG"]["base_url"])
    for post in app.config["BLOG"]["posts"]:
        url = url_for("post", year=post.revdate.year, month=post.revdate.month,
                      day=post.revdate.day)
        update = dt.datetime(year=post.revdate.year, month=post.revdate.month,
                             day=post.revdate.day)
        feed.add(post.title, post.to_html(), content_type="html",
                 author=app.config["BLOG"]["author"], updated=update,
                 url=urljoin(app.config["BLOG"]["base_url"], url))

    return feed.get_response()
