import json
import dataclasses
import functools


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


COSTS: dict[str, tuple[list[str], float]] = {
    "0": ([], 0),
    "1": ([], 1),
    "2": ([], 2),
    "3": ([], 3),
    "4": ([], 4),
    "5": ([], 5),
    "6": ([], 6),
    "7": ([], 7),
    "8": ([], 8),
    "9": ([], 9),
    "10": ([], 10),
    "11": ([], 11),
    "12": ([], 12),
    "15": ([], 15),

    "X": ([], .1),

    "B": (["B"], 1),
    "G": (["G"], 1),
    "R": (["R"], 1),
    "U": (["U"], 1),
    "W": (["W"], 1),

    "2B": (["B"], 1.49),
    "2G": (["G"], 1.49),
    "2R": (["R"], 1.49),
    "2U": (["U"], 1.49),
    "2W": (["W"], 1.49),

    "BP": (["B"], 1),
    "GP": (["G"], 1),
    "RP": (["R"], 1),
    "UP": (["U"], 1),
    "WP": (["W"], 1),

    "UB": (["U", "B"], 1),
    "BR": (["B", "R"], 1),
    "RG": (["R", "G"], 1),
    "GW": (["G", "W"], 1),
    "WU": (["W", "U"], 1),

    "WB": (["W", "B"], 1),
    "UR": (["U", "R"], 1),
    "BG": (["B", "G"], 1),
    "RW": (["R", "W"], 1),
    "GU": (["G", "U"], 1),
}


@dataclasses.dataclass
class Card:
    id: str
    title: str
    set_id: str
    order: int
    scryfall_uri: str
    img_uri: str
    cost: list[str] = None
    rarity: str = None
    card_type: str = None

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
            "cost": self.cost,
        }

    @functools.cached_property
    def color(self) -> str:
        if self.cost is None:
            return "L"

        colorset = set()
        for cost in self.cost:
            colors, _ = COSTS[cost]
            colorset.update(*colors)

        return ''.join(sorted(list(colorset)))

    @functools.cached_property
    def cmc(self) -> float:
        if self.cost is None:
            return -1

        out = 0

        for cost in self.cost:
            _, cmc = COSTS[cost]
            out += cmc

        return out


def load_set(name: str) -> list[Card]:
    with open(f"set_json/{name}.json", "r") as fh:
        cards_json = json.load(fh)

    return [Card(**data) for data in cards_json]
