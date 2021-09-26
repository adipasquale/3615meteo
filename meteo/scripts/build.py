import os
from distutils.dir_util import copy_tree
from meteo.meteofrance.fetch import fetch_bulletin_cotier_xml, fetch_bulletin_special_json
from meteo.meteofrance.bulletin_cotier import parse_bulletin_xml as parse_bulletin_cotier_xml, BULLETINS_CODES as BULLETINS_COTIERS_CODES
from meteo.meteofrance.bulletin_special import parse_bulletin_json as parse_bulletin_special_json, BULLETINS_CODES as BULLETINS_SPECIAUX_CODES
from itertools import groupby
import json
from meteo.lib.renderer import render_template, clear_build_and_tmp_dirs
import argparse

DIRNAME = os.path.dirname(__file__)
ROOT_PATH = os.path.join(DIRNAME, "..", "..")
BUILD_PATH = os.path.join(ROOT_PATH, "docs")

flatten = lambda x: [i for row in x for i in row]

def fetch_bulletin_cotier(code):
    bulletin_xml = fetch_bulletin_cotier_xml(code)
    with open(os.path.join(BUILD_PATH, "raw", f"{code}.xml"), "w") as f:
        f.write(bulletin_xml)


def parse_bulletin_cotier(code):
    with open(os.path.join(BUILD_PATH, "raw", f"{code}.xml"), "r") as f:
        bulletin_xml = f.read()
    parsed = parse_bulletin_cotier_xml(bulletin_xml.encode("utf-8"), code)
    with open(os.path.join(BUILD_PATH, "api", "bulletins_cotiers", f"{code}.json"), "w") as f:
        f.write(json.dumps(parsed, default=str))
    return parsed


def render_bulletin_cotier(bulletin):
    render_template(
        "bulletin-cotier.html.jinja",
        f"bulletin-{bulletin['code']}.html",
        { "bulletin": bulletin }
    )


def fetch_bulletin_special(code):
    bulletin_json = fetch_bulletin_special_json(code)
    if bulletin_json is None:
        # means there is no ongoing BMS for this coast
        return

    with open(os.path.join(BUILD_PATH, "raw", f"{code}.json"), "w") as f:
        f.write(bulletin_json)


def parse_bulletin_special(code):
    path = os.path.join(BUILD_PATH, "raw", f"{code}.json")
    if not os.path.exists(path):
        return None

    with open(path, "r") as f:
        bulletin_json = f.read()
    parsed = parse_bulletin_special_json(bulletin_json)
    with open(os.path.join(BUILD_PATH, "api", "bulletins_speciaux", f"{code}.json"), "w") as ff:
        ff.write(json.dumps(parsed, default=str))
    return parsed


def render_bulletin_special(bulletin):
    render_template(
        "bulletin-special.html.jinja",
        f"bulletin-special-{bulletin['code']}.html",
        { "bulletin": bulletin }
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-fetch", help="uses pre-existing XMLs as cache", action="store_true")
    args = parser.parse_args()
    clear_build_and_tmp_dirs(skip_raw=args.skip_fetch)
    copy_tree(os.path.join(ROOT_PATH, "static_assets"), BUILD_PATH)

    # FETCH
    if not args.skip_fetch:
        for code in BULLETINS_COTIERS_CODES:
            fetch_bulletin_cotier(code)
        for code in BULLETINS_SPECIAUX_CODES:
            fetch_bulletin_special(code)

    # PARSE
    bulletins_cotiers = [parse_bulletin_cotier(code) for code in BULLETINS_COTIERS_CODES]
    bulletins_speciaux = [parse_bulletin_special(code) for code in BULLETINS_SPECIAUX_CODES]
    bulletins_speciaux = flatten([b for b in bulletins_speciaux if b is not None])
    bulletins_cotiers_by_code_cote = {k: list(v) for k, v in groupby(bulletins_cotiers, lambda b: b["code_cote"])}
    bulletins_speciaux_by_code_cote = {k: list(v) for k, v in groupby(bulletins_speciaux, lambda b: b["code_cote"])}

    # RENDER API INDEXES
    with open(os.path.join(BUILD_PATH, "api", "bulletins_speciaux.json"), "w") as f:
        f.write(json.dumps(bulletins_speciaux, default=str))
    with open(os.path.join(BUILD_PATH, "api", "bulletins_cotiers.json"), "w") as f:
        f.write(json.dumps(bulletins_cotiers, default=str))

    # RENDER
    render_template(
        "index.html.jinja",
        "index.html",
        {
            "bulletins_cotiers_by_code_cote": bulletins_cotiers_by_code_cote,
            "bulletins_speciaux_by_code_cote": bulletins_speciaux_by_code_cote
        }
    )
    render_template(
        "api.html.jinja",
        "api.html",
        {
            "bulletins_cotiers": bulletins_cotiers,
            "bulletins_speciaux": bulletins_speciaux
        }
    )
    for bulletin in bulletins_cotiers:
        render_bulletin_cotier(bulletin)
    for bulletin in bulletins_speciaux:
        render_bulletin_special(bulletin)
