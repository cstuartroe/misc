import json
import dataclasses


MY_SETS = [
    "leb",
    "arn",
    "atq",
    "leg",
    "drk",
    "fem",
    "chr",

    # Ice Age block
    "ice",
    "hml",
    "all",

    # Mirage block
    "mir",
    "vis",
    "wth",

    "por",

    # Tempest block
    "tmp",
    "sth",
    "exo",

    # Odyssey block
    "ody",
    "tor",
    "jud",

    # Mirrodin block
    "mrd",
    "dst",
    "5dn",

    # Kamigawa block
    "chk",
    "bok",
    "sok",

    "9ed",

    # Ravnica block
    "rav",
    "gpt",
    "dis",

    "csp",

    # Time Spiral block
    "tsp",
    "plc",
    "fut",

    "10e",

    # Lorwyn-Shadowmoor block
    "lrw",
    "mor",
    "shm",
    "eve",

    # Alara block
    "ala",
    "con",
    "arb",

    # Zendikar block
    "zen",
    "wwk",
    "roe",

    # Scars of Mirrodin block
    "som",
    "mbs",
    "nph",

    # Innistrad block
    "isd",
    "dka",
    "avr",

    # Return to Ravnica block
    "rtr",
    "gtc",
    "dgm",
]


@dataclasses.dataclass
class Card:
    id: str
    title: str
    set_id: str
    order: int
    scryfall_uri: str
    img_uri: str
    rarity: str = None
    card_type: str = None
    color: str = None

    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "set_id": self.set_id,
            "order": self.order,
            "scryfall_uri": self.scryfall_uri,
            "img_uri": self.img_uri,
            "rarity": self.rarity,
            "card_type": self.card_type,
            "color": self.color,
        }


def load_set(name: str) -> list[Card]:
    with open(f"set_json/{name}.json", "r") as fh:
        cards_json = json.load(fh)

    return [Card(**data) for data in cards_json]
