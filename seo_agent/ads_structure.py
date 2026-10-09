"""Leser data/ads_keywords.txt (kampanje → annonsegruppe → søkeord).
[ord] = eksakt samsvar, ellers frasesamsvar. Slutt-* = samsvarstype ikke bekreftet.
Brukes som kart for «rød tråd» selv når Google Ads-API ikke er koblet til."""
import re

HEAD = re.compile(r"^(.*?)\s*\((\d+)(\s+søkeord)?\)\s*$")


def parse(path="data/ads_keywords.txt"):
    camps, camp, grp = [], None, None
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        m = HEAD.match(line)
        if m and m.group(3):
            camp = {"campaign": m.group(1), "declared": int(m.group(2)), "ad_groups": []}
            camps.append(camp)
            grp = None
        elif m:
            grp = {"ad_group": m.group(1), "declared": int(m.group(2)), "keywords": []}
            camp["ad_groups"].append(grp)
        else:
            if grp is None:  # kampanje uten annonsegrupper
                grp = {"ad_group": "(ingen)", "declared": camp["declared"], "keywords": []}
                camp["ad_groups"].append(grp)
            for k in line.split(","):
                k = k.strip()
                if not k:
                    continue
                unconfirmed = k.endswith("*")
                k = k.rstrip("*")
                exact = k.startswith("[") and k.endswith("]")
                grp["keywords"].append({"kw": k.strip("[]"), "match": "eksakt" if exact else "frase",
                                        **({"match_unconfirmed": True} if unconfirmed else {})})
    return camps
