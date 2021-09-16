import os
# from re import template
from jinja2 import Environment, PackageLoader, select_autoescape
from distutils.dir_util import copy_tree
from meteo.meteofrance.fetch import fetch_bulletin_cotier_xml, fetch_bulletin_special_json
from meteo.meteofrance.bulletin_cotier import parse_bulletin_xml as parse_bulletin_cotier_xml, BULLETINS_CODES as BULLETINS_COTIERS_CODES
from meteo.meteofrance.bulletin_special import parse_bulletin_json as parse_bulletin_special_json, BULLETINS_CODES as BULLETINS_SPECIAUX_CODES
import re
from itertools import groupby
import shutil

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


def clear_build_and_tmp_dirs():
    for dir_name in ["tmp", "docs"]:
        path = os.path.join(ROOT_PATH, dir_name)
        if os.path.exists(path):
            shutil.rmtree(path)
        os.makedirs(path)


def fetch_and_parse_bulletin_cotier(code):
    bulletin_xml = fetch_bulletin_cotier_xml(code)
    bulletin_parsed = parse_bulletin_cotier_xml(bulletin_xml.encode("utf-8"), code)
    bulletin_parsed["raw_xml"] = bulletin_xml
    return bulletin_parsed


def render_bulletin_cotier(bulletin):
    xml_filename = f"{bulletin['code']}.xml"
    with open(os.path.join(BUILD_PATH, xml_filename), "w") as f:
        f.write(bulletin["raw_xml"])
    render_template(
        "bulletin-cotier.html.jinja",
        f"bulletin-{bulletin['code']}.html",
        {
                "bulletin": bulletin,
                "path_xml": xml_filename,
                "url_meteofrance": bulletin["url_meteofrance"]
        }
    )


def fetch_and_parse_bulletin_special(code):
    bulletin_json = fetch_bulletin_special_json(code)
    if bulletin_json is None:
        # means there is no ongoing BMS for this coast
        return

    bulletin_parsed = parse_bulletin_special_json(bulletin_json)
    bulletin_parsed["raw_json"] = bulletin_json
    return bulletin_parsed


def render_bulletin_special(bulletin):
    json_filename = f"{bulletin['code']}.json"
    with open(os.path.join(BUILD_PATH, json_filename), "w") as f:
        f.write(bulletin["raw_json"])

    render_template(
        "bulletin-special.html.jinja",
        f"bulletin-special-{bulletin['code']}.html",
        {
                "bulletin": bulletin,
                "path_json": json_filename
        }
    )


if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--use-cache', const=True, action='store_const')
    # args = parser.parse_args()
    clear_build_and_tmp_dirs()
    # TODO: cleanup old built files
    copy_tree(os.path.join(ROOT_PATH, "static_assets"), BUILD_PATH)

    bulletins_cotiers = [fetch_and_parse_bulletin_cotier(code) for code in list(BULLETINS_COTIERS_CODES)]
    bulletins_speciaux = [fetch_and_parse_bulletin_special(code) for code in BULLETINS_SPECIAUX_CODES]
    bulletins_speciaux = [b for b in bulletins_speciaux if b is not None]
    bulletins_cotiers_by_code_cote = {k: list(v) for k, v in groupby(bulletins_cotiers, lambda b: b["code_cote"])}
    bulletins_speciaux_by_code_cote = {k: list(v) for k, v in groupby(bulletins_speciaux, lambda b: b["code_cote"])}

    render_template(
        "index.html.jinja",
        f"index.html",
        {
            "bulletins_cotiers_by_code_cote": bulletins_cotiers_by_code_cote,
            "bulletins_speciaux_by_code_cote": bulletins_speciaux_by_code_cote
        }
    )

    for bulletin in bulletins_cotiers:
        render_bulletin_cotier(bulletin)
    for bulletin in bulletins_speciaux:
        render_bulletin_special(bulletin)
