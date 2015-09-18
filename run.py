import fnmatch
import os
import subprocess
import sys

import yaml
from flask_frozen import Freezer

from blog import app
from config import config
from post import Post


def load(*args, freeze=False):
    for basedir in args:
        for root, __, fnames in os.walk(basedir):
            for fname in fnmatch.filter(fnames, "*.adoc"):
                path = os.path.join(root, fname)
                try:
                    yield Post(path, freeze=freeze)
                except Exception as e:
                    raise RuntimeError("Error loading", path) from e

app.config["BLOG"] = config


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "build":
        posts = sorted(load("posts", freeze=True),
                       key=lambda x: x.revdate, reverse=True)
        app.config["BLOG"]["posts"] = posts
        app.config["FREEZER_BASE_URL"] = app.config["BLOG"]["base_url"]
        app.config["FREEZER_DESTINATION"] = "../build"

        freezer = Freezer(app)
        freezer.freeze()
        subprocess.check_call("./fix.sh")
    else:
        posts = sorted(load("posts", "drafts", freeze=False),
                       key=lambda x: x.revdate, reverse=True)
        app.config["BLOG"]["posts"] = posts
        app.run(debug=True)
