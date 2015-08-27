import fnmatch
import itertools
import os
import sys

import yaml
from flask_frozen import Freezer

from blog import app
from post import Post


def load(basedir):
    for root, __, fnames in os.walk(basedir):
        for fname in fnmatch.filter(fnames, "*.adoc"):
            yield Post(os.path.join(root, fname))

with open("config.yml") as fin:
    app.config["BLOG"] = yaml.load(fin)


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "build":
        posts = sorted(itertools.chain(load("posts"), load("drafts")),
                       key=lambda x: x.revdate, reverse=True)
        app.config["BLOG"]["posts"] = posts
        app.config["FREEZER_BASE_URL"] = app.config["BLOG"]["base_url"]
        app.config["FREEZER_DESTINATION"] = "../build"

        freezer = Freezer(app)
        freezer.freeze()
    else:
        posts = sorted(load("posts"), key=lambda x: x.revdate, reverse=True)
        app.config["BLOG"]["posts"] = posts
        app.run(debug=True)
