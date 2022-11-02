import json
from typing import Iterable

import requests
from tqdm import tqdm
from bs4 import BeautifulSoup

from utils import FEATURES_FILE, Feature, CategoryMap, load_features, dump_features

CALS = "https://cals.info"
CALS_FEATURE_URI = CALS + "/feature/%s/"


# Some CALS features have different names from the corresponding WALS map
# This is a map from CALS feature names to WALS map names
FEATURE_NAME_MAP = {
    "Position of Negative Morpheme With Respect to Subject, Object and Verb":
        "Position of Negative Word With Respect to Subject, Object, and Verb",
}

# Obviously there was some manual data entry involved in the making of CALS
# These are typo corrections in category names
CATEGORY_NAME_MAP = {
    "No voicing constrast": "No voicing contrast",
    "Fixed stress": "Fixed stress (no weight-sensitivity)",
    "Pharyngeals and 'th'": 'Pharyngeals and "th"',
}


def bs(uri):
    res = requests.get(uri)
    return BeautifulSoup(res.content, "html.parser")


def pull_wals_map(map_id: str) -> CategoryMap:
    res = requests.get(
        "https://wals.info/values",
        params={
            "parameter": map_id,
            "sEcho": "1",
        },
        headers={
            "X-Requested-With": "XMLHttpRequest",
        },
    )

    data = json.loads(res.content)

    out = {}
    for row in data["aaData"]:
        name = BeautifulSoup(row[0], "html.parser").text.strip()
        category = BeautifulSoup(row[1], "html.parser").text.strip()

        out[category] = out.get(category, set()) | {name}

    return out


def pull_wals_chapter(wals_link: str, feature_name: str) -> CategoryMap:
    feature_name = FEATURE_NAME_MAP.get(feature_name, feature_name)

    soup = bs(wals_link)
    for a in soup.find("div", {"class": "well-small"}).find_all("a"):
        if a.text == feature_name:
            map_id = a["href"].split("/")[-1]
            return pull_wals_map(map_id)

    raise ValueError(f"No map found: {wals_link} {feature_name}")


def pull_cals_list(uri) -> Iterable[str]:
    soup = bs(uri)

    conlang_rows = soup.find("div", {"id": "main"}).table.find_all("tr")[3].table.find_all("tr", recursive=False)[1:]

    for i, row in enumerate(conlang_rows):
        out = row.td.a["href"].split("/")[2]
        if out != "":
            yield out


def pull_cals_categories(soup: BeautifulSoup) -> CategoryMap:
    tr = soup.table.find_all("tr")[1]
    rows = tr.td.table.find_all("tr")[1:]

    return {
        CATEGORY_NAME_MAP.get(row.td.a.text, row.td.a.text).strip(): set(pull_cals_list(CALS + row.td.a["href"]))
        for row in rows
    }


def pull_feature(feature_id: str) -> Feature:
    soup = bs(CALS_FEATURE_URI % feature_id)

    main = soup.find("div", {"id": "main"})
    h1 = main.h1

    feature_name = next(h1.children).strip()
    feat = Feature(
        feature_name,
        pull_cals_categories(main),
    )

    if h1.sup is not None:
        wals_link = h1.sup.a["href"]
        feat.natlangs = pull_wals_chapter(wals_link, feature_name)

    return feat


def pull_features(filename: str = FEATURES_FILE, caching: bool = True) -> dict[str, Feature]:
    features = load_features(filename)

    soup = bs(CALS_FEATURE_URI % 'p1')
    treelist = soup.find("ul", {"class": "treelist"})

    lis = [
        li
        for ul in treelist.find_all("ul")
        for li in ul.find_all("li")
    ]

    for li in tqdm(lis):
        feature_id = li.a["href"].split("/")[1]

        if feature_id not in features:
            features[feature_id] = pull_feature(feature_id)

            if caching:
                dump_features(features, filename)

    return features


if __name__ == "__main__":
    pull_features()
