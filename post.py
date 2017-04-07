""" Wrapper around Ruby asciidoctor functionality """

import datetime as dt
import re
import subprocess
import tempfile

from config import config

metadata_regex = re.compile(r"^:(.*?): *(.*)$")

def get_asciidoc_metadata(path: str) -> dict:
    metadata = {}
    with open(path) as fin:
        for line in fin:
            if line.startswith("= ") and "title" not in metadata:
                metadata["title"] = line[2:].strip()

            m = metadata_regex.match(line)
            if m is not None:
                name, data = m.groups()
                if name == "keywords":
                    data = [s.strip() for s in data.split(",")]
                elif name == "revdate":
                    data = dt.datetime.strptime(data, "%Y-%m-%d").date()
                metadata[name] = data
    return metadata

def convert(fname) -> str:
    args = ["asciidoctor", "--out-file", "-", "--no-header-footer", fname]
    p = subprocess.Popen(args, stdout=subprocess.PIPE)
    stdout, __ = p.communicate()

    return stdout.decode("utf-8")

class Post(object):
    def __init__(self, path: str):
        self.path = path
        self.metadata = get_asciidoc_metadata(path)
        self.needs_pygments = "source-highlighter" in self.metadata
        self.needs_mathjax = "stem" in self.metadata

        # set required fields
        for f in ["revdate", "category", "title", "description"]:
            setattr(self, f, self.metadata.pop(f))

        # set optional fields
        for f in ["keywords"]:
            if f in self.metadata:
                setattr(self, f, self.metadata.pop(f))

    def to_html(self) -> str:
        with open(self.path) as fin:
            text = fin.read()

        text = text.replace("link:/", "link:" + config["base_path"]) \
                   .replace("image::/", "image::" + config["base_path"]) \
                   .replace("image:/", "image:" + config["base_path"])
        with tempfile.NamedTemporaryFile() as fout:
            fout.write(text.encode())
            fout.flush()
            return convert(fout.name)
