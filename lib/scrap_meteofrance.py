import requests
from lxml.cssselect import CSSSelector
from lxml.html import fromstring, tostring
import js2py
import xml.etree.ElementTree as ET
import re


def mfsession_to_token(mfsession):
    return js2py.eval_js("""
    const mfsession = "%s";
    const o = decodeURIComponent(mfsession);
    const token = o.replace(/[a-zA-Z]/g, function(e) {
        var t = e <= "Z" ? 65 : 97;
        return String.fromCharCode(t + (e.charCodeAt(0) - t + 13) %% 26)
    })
    token
    """ % (mfsession, ))


def get_token():
    r = requests.get("https://meteofrance.com/meteo-marine/port-camargue-saint-raphael/BMSCOTE-02-02")
    return mfsession_to_token(r.cookies["mfsession"])


def fetch_bulletin_xml(code):
    token = get_token()
    headers = {
        "Authorization": f"Bearer {token}"
    }
    r = requests.get(
        "https://rpcache-aa.meteofrance.com/internet2018client/2.0/report?domain=%s&report_type=marine&report_subtype=BMR_cote_fr&format=xml" % (code, ),
        headers=headers
    )
    if r.status_code != 200:
        print(r)
        raise
    return r.text
