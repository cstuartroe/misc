import json
from download import Segment, Inventory


def has_aspiration_contrast(inv: Inventory):
    for segment in inv.consonants:
        if segment.ipa.endswith("ʰ"):
            if any(s.ipa == segment.ipa[:-1] for s in inv.consonants):
                return True

    return False


def has_h(inv: Inventory):
    for segment in inv.consonants:
        if segment.ipa in "hxɦ":
            return True

    return False


if __name__ == "__main__":
    with open("inventories.json", "r") as fh:
        data = json.load(fh)

    inventories = [
        Inventory.from_dict(d)
        for d in data
    ]

    aspiration_no_h_invs = []

    for inv in inventories:
        if has_aspiration_contrast(inv):
            if not has_h(inv):
                aspiration_no_h_invs.append(inv)

    aspiration_no_h_invs.sort(key=lambda inv: inv.languageName)

    for inv in aspiration_no_h_invs:
        print((inv.id, inv.title, inv.languageName))
        print()
