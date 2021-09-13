import os
# from re import template
import pystache
from distutils.dir_util import copy_tree
from scrap_meteofrance import fetch_bulletin_xml
from meteofrance import parse_bulletin_xml
import collections.abc
import re

DIRNAME = os.path.dirname(__file__)

def apply_recursive(func, obj):
    if isinstance(obj, dict):  # if dict, apply to each key
        return {k: apply_recursive(func, v) for k, v in obj.items()}
    elif isinstance(obj, list):  # if list, apply to each element
        return [apply_recursive(func, elem) for elem in obj]
    else:
        return func(obj)

def create_tmp_directories():
    for dir_name in ["tmp", "build"]:
        path = os.path.join(DIRNAME, '..', dir_name)
        if not os.path.exists(path):
            os.makedirs(path)


def render_template(template_filename, html_filename, vars):
    create_tmp_directories
    template_path = os.path.join(DIRNAME, '..', template_filename)
    renderer = pystache.Renderer()
    rendered_html = renderer.render_path(
        template_path, vars
    )
    index_path = os.path.join(DIRNAME, '..', 'build', html_filename)
    file = open(index_path, 'w')
    file.write(rendered_html)
    file.close()


def copy_assets():
    copy_tree(
        os.path.join(DIRNAME, "..", "static_assets"),
        os.path.join(DIRNAME, "..", "build")
    )
    print("rebuild done.")


def create_tmp_directories():
    for dir_name in ["tmp", "build"]:
        path = os.path.join(DIRNAME, '..', dir_name)
        if not os.path.exists(path):
            os.makedirs(path)


def replace_linebreaks_with_br(text):
    print(text)
    if "\n" in text:
        print("here")
        return re.sub("\n", "<br />", text)
    else:
        return text


if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--use-cache', const=True, action='store_const')
    # args = parser.parse_args()
    create_tmp_directories()
    bulletin_xml = fetch_bulletin_xml("BMRCOTE-02-02")
    bulletin_parsed = parse_bulletin_xml(bulletin_xml.encode("utf-8"))
    bulletin_html_ready = apply_recursive(lambda v: replace_linebreaks_with_br(v), bulletin_parsed)
    render_template("meteo.mustache", "meteo.html", { "bulletin": bulletin_html_ready })
