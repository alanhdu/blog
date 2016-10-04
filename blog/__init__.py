import datetime as dt
import math
from urllib.parse import urljoin
from functools import partial

from flask import Flask, render_template, abort, request, url_for
from werkzeug.contrib.atom import AtomFeed
import toolz

app = Flask(__name__)

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
    groups = toolz.pipe(app.config["BLOG"]["posts"],
                        partial(toolz.groupby, lambda x: x.category),
                        partial(toolz.valmap,
                                lambda group: sorted(group,
                                                     key=lambda x: x.revdate,
                                                     reverse=True)))
    return render_template("categories.html", groups=groups)

@app.route("/post/<int:year>/<int:month>/<int:day>/")
def post(year, month, day):
    for p in app.config["BLOG"]["posts"]:
        if p.revdate == dt.date(year, month, day):
            return render_template("post.html", post=p)
    abort(404)

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
