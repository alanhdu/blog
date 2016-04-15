import urllib.parse
import yaml

with open("config.yml") as fin:
    config = yaml.load(fin)
config["base_path"] = urllib.parse.urlparse(config["base_url"]).path
