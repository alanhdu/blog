import datetime as dt

from flask import Flask, render_template, abort, redirect, url_for

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


def get_post(date: dt.date) -> "Optional[Post]":
    for p in app.config["BLOG"]["posts"]:
        if p.metadata.revdate == date:
            return p


@app.route("/<int:year>/<int:month>/<int:day>/")
def post(year, month, day):
    post = get_post(dt.date(year=year, month=month, day=day))
    if post is None:
        abort(404)

    return render_template("post.html", post=post)
