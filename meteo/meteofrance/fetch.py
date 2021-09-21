import requests
import js2py


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

TOKEN = get_token()

def fetch_file_meteofrance(path):
    headers = { "Authorization": f"Bearer {TOKEN}" }
    r = requests.get(
        f"https://rpcache-aa.meteofrance.com/internet2018client/2.0/{path}",
        headers=headers
    )
    if r.status_code == 204: # no content
        return None
    if r.status_code != 200:
        print(r)
        raise
    return r.text


def fetch_bulletin_cotier_xml(code):
    return fetch_file_meteofrance(
        "report?domain=%s&report_type=marine&report_subtype=BMR_cote_fr&format=xml" % (code, )
    )

def fetch_bulletin_special_json(code):
    return fetch_file_meteofrance(
        "report?domain=%s&report_type=marine&report_subtype=BMS_cote_fr&format=json" % (code, )
    )
