from unittest.main import main
import re
import json
import dateutil.parser
import itertools


"""
    parses the meteofrance bulletin special json to dicts that look like:
    [
        {
            'numero': '346',
            'titre': 'BMS COTE MEDITERRANEE',
            'type_avis': 'AVIS DE GRAND FRAIS',
            'code': 'BMSCOTE-02',
            "code_cote": "02",
            'blocks':
            [
                {
                    'titre': 'PROVENCE : de Port-Camargue au Cap Cépet.',
                    'begin_time': datetime.datetime(2021, 9, 15, 3, 2, 26, tzinfo=tzutc()),
                    'code': 'BMSCOTE-02-02',
                    'end_time': datetime.datetime(2021, 9, 15, 15, 0, tzinfo=tzutc()),
                    'texts': [
                        "En cours et valable jusqu'au mercredi 15 septembre à 15H00 UTC",
                        'VENT : Sud-Est 7. Rafales'
                    ]
                }
            ]
        }
    ]
"""

KNOWN_BULLETIN_TAGS = set(["report_type", "report_subtype", "domain_id", "report_title", "update_time", "end_validity_time", "text_bloc_item"])

BULLETINS_CODES = ["BMSCOTE-01", "BMSCOTE-02"]

def parse_first_block(block):
    if block["bloc_title"] != "" or block["begin_time"] != "" or block["end_time"] != "":
        raise Exception(f"main block has non empty title or time")

    if len(block["text_items"]) < 2:
        raise Exception(f"main block has less than 2 text items")

    main_block = {}

    texts = [t["title"] for t in block["text_items"]]

    numero_regex = r"^BMS Côte numéro ([0-9]+)"
    text_numero = next((t for t in texts if re.match(numero_regex, t)))
    if text_numero:
        main_block["numero"] = re.match(numero_regex, text_numero).groups()[0]

    type_avis_regex = r"^AVIS DE [A-Z \-]+\.?"
    text_type_avis = next((t for t in texts if re.match(type_avis_regex, t, re.IGNORECASE)))
    if text_type_avis:
        main_block["type_avis"] = text_type_avis.strip(" .")

    return main_block

def parse_secondary_block(block):
    if len(block["domain_id"]) < 2:
        raise Exception(f"block has less than 2 domain_ids")

    return {
        "code": block["domain_id"][-1],
        "titre": block["bloc_title"],
        "begin_time": dateutil.parser.isoparse(block["begin_time"]) if "begin_time" in block else None,
        "end_time": dateutil.parser.isoparse(block["end_time"]) if "end_time" in block else None,
        "texts": [t["text"].strip(" .") for t in block["text_items"] if "text" in t]
    }

def parse_block_pair(first_block, secondary_blocks, parsed):
    main_block = parse_first_block(first_block)
    return {
        "code": parsed["domain_id"],
        "code_cote": re.match(r"BMSCOTE-(\d+)", parsed["domain_id"]).groups()[0],
        "titre": parsed["report_title"],
        "numero": main_block["numero"],
        "type_avis": main_block["type_avis"],
        "blocs": [parse_secondary_block(b) for b in secondary_blocks]
    }

def get_main_block_indexes(blocks):
    text_items_all = [list(filter(lambda t: t != {}, b["text_items"])) for b in blocks]
    titles = [list(map(lambda t: t.get("title", t.get("text")), text_items_block)) for text_items_block in text_items_all]
    titles_joined = list(map(lambda t: " ".join(t), titles))
    bools = list(enumerate(["BMS Côte numéro" in t for t in titles_joined]))
    return [e[0] for e in bools if e[1]]

def parse_bulletin_json(raw_json):
    parsed = json.loads(raw_json)

    unknown_tags = set(parsed.keys()) - KNOWN_BULLETIN_TAGS
    if len(unknown_tags) > 0:
        raise Exception(f"unknown bulletin special tag {list(unknown_tags)[0]}")

    if len(parsed["text_bloc_item"]) < 2:
        raise Exception(f"less than 2 text_bloc_item in BMS")

    blocks = parsed["text_bloc_item"]
    main_block_indexes = get_main_block_indexes(blocks) + [None]
    index_pairs = zip(main_block_indexes, main_block_indexes[1:])

    return [parse_block_pair(blocks[i1], blocks[i1 + 1:i2], parsed) for i1, i2 in index_pairs]
