""" Wrapper around Ruby asciidoctor functionality """

from collections import namedtuple
import datetime as dt
import re
import subprocess
import tempfile
import urllib.parse

from config import config

converter = "asciidoctor"
metadata_regex = re.compile(r"^:(.*?): *(.*)$")

base_path = urllib.parse.urlparse(config["base_url"]).path

fields = ["title", "category", "keywords", "revdate", "description", "path",
          "freeze"]

class Post(namedtuple("Post", fields)):
    def __new__(cls, path, freeze=False):
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

        return super().__new__(cls, freeze=freeze, **metadata)

    def to_html(self) -> str:
        if self.freeze:
            with open(self.path) as fin:
                text = fin.read()
            with tempfile.NamedTemporaryFile() as fout:
                text = text.replace("link:/", "link:" + base_path + "/")
                fout.write(text.encode())
                fout.flush()

                return convert(fout.name)
        else:
            return convert(self.path)

def convert(fname) -> str:
    args = [converter, "--out-file", "-", "--no-header-footer", fname]
    p = subprocess.Popen(args, stdout=subprocess.PIPE)
    stdout, __ = p.communicate()

    return stdout.decode("utf-8")
