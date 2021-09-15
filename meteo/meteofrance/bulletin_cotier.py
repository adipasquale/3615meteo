from lxml import etree
import re
import csv
import os

"""
    parses the meteofrance bulletin XMLs to dicts that look like:
    {
        "code": "BMRCOTE-02-02",
        "code_cote": "02",
        "title": "Bulletin côte "Port Camargue - Saint Raphaël" midi",
        "chapeau": "Bulletin côtier pour la bande des 20 milles, ...",
        "avis_special": "Pas d'avis de vent fort en cours ni prévu.",
        "echeances": [
            {
                "titre": "Situation générale le lundi 13 septembre 2021...",
                "regions": [
                    {
                        "situation": "Faible gradient de pression 1015 hPa..."
                    }
                ]
            },
            {
                "titre": "Observations le lundi 13 septembre 2021 à 09H00...",
                "regions": [
                    {
                        "observations": [
                            {"observation": "Cap Camarat : vent Est-Sud-Est 4 nœuds...."}
                        ]
                    }
                ]
            },
            {
                "titre": "Prévisions pour l'après-midi du lundi...",
                "regions": [
                    {
                        "previsions": {
                            "vent": "- à l'ouest de Sicié : Sud-Est 3 à 4....",
                            "mer": "belle.",
                            "houle": "non significative",
                            "temps": "nuageux",
                            "visibilite": "bonne"
                        }
                    }
                ]
            },
            ...
        ],
        "pied": "Prochain bulletin le lundi 13 septembre 2021..."
    }
"""

REGION_TAGS = {
    "vent": "VENT",
    "mer": "MER",
    "houle": "HOULE",
    "TS": "TEMPS",
    "visi": "VISIBILITE"
}
KNOWN_BULLETIN_TAGS = set(["titreBulletin", "uniteBulletin", "chapeauBulletin", "bulletinSpecial", "echeance", "piedBulletin"])
KNOWN_ECHEANCE_TAGS = set(["titreEcheance", "region"])
KNOWN_REGION_TAGS = set(list(REGION_TAGS.keys()) + ["observation", "situation"])

DIRNAME = os.path.dirname(__file__)

f = open(os.path.join(DIRNAME, "bulletins_cotiers.csv"))
BULLETINS = list(csv.DictReader(f))
f.close()
BULLETINS_BY_CODE = {b["code"]: b for b in BULLETINS}
BULLETINS_CODES = BULLETINS_BY_CODE.keys()


def parse_echeance_region(elt):
    region_tags = set([e.tag for e in etree.XPath("./*")(elt)])
    unknown_tags = region_tags - KNOWN_REGION_TAGS
    if len(unknown_tags) > 0:
        raise Exception(f"unknown region tag {list(unknown_tags)[0]}")

    region = {}
    situationElts = etree.XPath("./situation")(elt)
    if len(situationElts) == 1:
        region["situation"] = situationElts[0].text.strip()
    observationElts = etree.XPath("./observation")(elt)
    if len(observationElts) >= 1:
        region["observations"] = [{"observation": e.text.strip()} for e in observationElts]
    if any([len(etree.XPath(f"./{tag}")(elt)) > 0 for tag in REGION_TAGS.keys()]):
        region["previsions"] = {}
    for tag, label in REGION_TAGS.items():
        valueElts = etree.XPath(f"./{tag}")(elt)
        if len(valueElts) == 1:
            region["previsions"][label.lower()] = re.sub(rf"^{label} :[\n ]", "", valueElts[0].text.strip())
    return region

def parse_echeance(elt):
    echeance_tags = set([e.tag for e in etree.XPath("./*")(elt)])
    unknown_tags = echeance_tags - KNOWN_ECHEANCE_TAGS
    if len(unknown_tags) > 0:
        raise Exception(f"unknown echeance tag {list(unknown_tags)[0]}")

    return {
        "titre": etree.XPath("./titreEcheance")(elt)[0].text.strip(),
        "regions": [parse_echeance_region(e) for e in etree.XPath("./region")(elt)]
    }

def parse_bulletin_xml(raw_xml, code):
    doc = etree.fromstring(raw_xml)
    bulletin_tags = set([e.tag for e in etree.XPath("/bulletin/*")(doc)])
    unknown_tags = bulletin_tags - KNOWN_BULLETIN_TAGS
    if len(unknown_tags) > 0:
        raise Exception(f"unknown bulletin tag {list(unknown_tags)[0]}")

    title = etree.XPath("/bulletin/titreBulletin")(doc)[0].text.strip()
    chapeau = etree.XPath("/bulletin/chapeauBulletin")(doc)[0].text.strip()
    avis_special = etree.XPath("/bulletin/bulletinSpecial")(doc)[0].text.strip()
    echeances = [parse_echeance(e) for e in etree.XPath("/bulletin/echeance")(doc)]
    pied = etree.XPath("/bulletin/piedBulletin")(doc)[0].text.strip()

    return {
        "code": code,
        "nom": BULLETINS_BY_CODE[code]["nom"],
        "code_cote": BULLETINS_BY_CODE[code]["code_cote"],
        "url_meteofrance": BULLETINS_BY_CODE[code]["url_meteofrance"],
        "titre": title,
        "chapeau": chapeau,
        "avis_special": avis_special,
        "echeances": echeances,
        "pied": pied
    }
