
import yaml

from blog import app

with open("config.yml") as fin:
    app.config["BLOG"] = yaml.load(fin)

if __name__ == "__main__":
    app.run(debug=True)
