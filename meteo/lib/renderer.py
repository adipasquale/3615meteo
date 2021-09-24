import os
from jinja2 import Environment, PackageLoader, select_autoescape
import re
import glob

DIRNAME = os.path.dirname(__file__)
JINJA_ENV = Environment(
    loader=PackageLoader("meteo"),
    autoescape=select_autoescape()
)
ROOT_PATH = os.path.join(DIRNAME, "..", "..")
BUILD_PATH = os.path.join(ROOT_PATH, "docs")


def linebreaks_to_br(text):
    return re.sub("\n", "<br />", text)

JINJA_ENV.filters["linebreaks_to_br"] = linebreaks_to_br


def render_template(template_filename, html_filename, vars):
    template = JINJA_ENV.get_template(template_filename)
    html = template.render(**vars)
    html_path = os.path.join(BUILD_PATH, html_filename)
    with open(html_path, 'w') as f:
        f.write(html)


def clear_build_and_tmp_dirs(skip_raw=False):
    dirs = [
        "tmp", "docs/api/bulletins_speciaux", "docs/api/bulletins_cotiers",
        (None if skip_raw else "docs/raw"),
        "docs"
    ]
    for dir_name in [d for d in dirs if d is not None]:
        path = os.path.join(ROOT_PATH, dir_name)
        if os.path.exists(path):
            for ext in ["html", "json", "xml", "png"]:
                for f in glob.glob(os.path.join(path, f"*.{ext}")):
                    os.remove(f)
        else:
            os.makedirs(path)
