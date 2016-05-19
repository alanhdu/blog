import glob
import os

import click
from flask_frozen import Freezer

from blog import app
from config import config
from post import Post

def load(dirs):
    for basedir in dirs:
        for path in glob.iglob(os.path.join(basedir, "**.adoc")):
            try:
                yield Post(path)
            except Exception as e:
                raise RuntimeError("Error loading", path) from e

app.config["BLOG"] = config


@click.group()
def cli():
    pass


@cli.command()
def serve():
    """Host blog on http://localhost:5000"""
    app.config["BLOG"]["posts"] = sorted(load(["posts", "drafts"]),
                                         key=lambda post: post.revdate,
                                         reverse=True)
    app.config["BLOG"]["base_path"] = "/"
    app.run(debug=True)


@cli.command()
def build():
    """Build blog"""
    app.config["BLOG"]["posts"] = sorted(load(["posts"]),
                                         key=lambda post: post.revdate,
                                         reverse=True)
    app.config["FREEZER_BASE_URL"] = app.config["BLOG"]["base_url"]
    app.config["FREEZER_DESTINATION"] = "../build"

    app.static_url_path = app.config["BLOG"]["base_path"] + "static/"

    freezer = Freezer(app)
    freezer.freeze()


if __name__ == "__main__":
    cli()
