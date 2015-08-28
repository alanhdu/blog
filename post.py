""" Wrapper around Ruby asciidoctor functionality """

from collections import namedtuple
import datetime as dt
import re
import subprocess

converter = "asciidoctor"
metadata_regex = re.compile(r"^:(.*?): *(.*)$")

fields = ["title", "category", "keywords", "revdate", "description", "path"]

class Post(namedtuple("Post", fields)):
    def __new__(cls, path):
        metadata = {"path": path}

        with open(path) as fin:
            for line in fin:
                if line.startswith("= "):
                    metadata["title"] = line[2:].strip()

                m = metadata_regex.match(line)
                if m is not None:
                    name, data = m.groups()
                    if name == "keywords":
                        data = [s.strip() for s in data.split(",")]
                    elif name == "revdate":
                        data = dt.datetime.strptime(data, "%Y-%m-%d").date()

                    metadata[name] = data

        for key in {"stem", "source-highlighter"}:
            metadata.pop(key, None)

        return super().__new__(cls, **metadata)

    def to_html(self) -> str:
        args = [converter, "--out-file", "-", "--no-header-footer", self.path]
        p = subprocess.Popen(args, stdout=subprocess.PIPE)
        stdout, __ = p.communicate()
        return stdout.decode("utf-8")
