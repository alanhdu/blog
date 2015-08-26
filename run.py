import fnmatch
import os

import yaml

from blog import app
from post import Post


def load(basedir):
    for root, __, fnames in os.walk(basedir):
        for fname in fnmatch.filter(fnames, "*.adoc"):
            yield Post(os.path.join(root, fname))

posts = list(load("posts"))

with open("config.yml") as fin:
    app.config["BLOG"] = yaml.load(fin)

app.config["BLOG"]["posts"] = posts

if __name__ == "__main__":
    app.run(debug=True)
