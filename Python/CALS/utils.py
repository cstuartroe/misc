import os
import json
from typing import Optional
from dataclasses import dataclass


FEATURES_FILE = "features.json"

CategoryMap = dict[str, set[str]]


def cm2json(cm: CategoryMap):
    return {
        cat: sorted(list(langs))
        for cat, langs in cm.items()
    }


def json2cm(data: dict[str, list[str]]):
    return {
        cat: set(langs)
        for cat, langs in data.items()
    }


@dataclass
class Feature:
    name: str
    conlangs: CategoryMap
    natlangs: Optional[CategoryMap] = None

    def to_json(self):
        return {
            "name": self.name,
            "conlangs": cm2json(self.conlangs),
            "natlangs": self.natlangs and cm2json(self.natlangs),
        }

    @staticmethod
    def from_json(data: dict):
        return Feature(
            name=data["name"],
            conlangs=json2cm(data["conlangs"]),
            natlangs=data["natlangs"] and json2cm(data["natlangs"]),
        )


def dump_features(features: dict[str, Feature], filename: str = FEATURES_FILE):
    jsonified = {
        ID: f.to_json()
        for ID, f in features.items()
    }

    with open(filename, "w") as fh:
        json.dump(jsonified, fh, indent=2)


def load_features(filename: str = FEATURES_FILE) -> dict[str, Feature]:
    if not os.path.exists(filename):
        return {}

    with open(filename, "r") as fh:
        data = json.load(fh)

    return {
        ID: Feature.from_json(d)
        for ID, d in data.items()
    }
