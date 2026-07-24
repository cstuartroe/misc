import dataclasses
import json

import download


@dataclasses.dataclass
class SetStats:
    id: str
    num_commons: int = 0
    num_uncommons: int = 0
    num_rares: int = 0
    num_basic_lands: int = 0


if __name__ == "__main__":
    card_names_to_sets = {}
    set_stats = []

    for set_id in download.MY_SETS:
        with open(f"set_json/{set_id}.json", "r") as fh:
            set_json = json.load(fh)

        stats = SetStats(id=set_id)
        set_stats.append(stats)

        for card in set_json:
            if card["title"] in card_names_to_sets:
                print(f"{card["title"]:<25} in {card_names_to_sets[card["title"]]} and {set_id}")
            elif card["title"] in ("Plains", "Mountain", "Forest", "Island", "Swamp"):
                pass
            else:
                card_names_to_sets[card["title"]] = set_id

            if card["card_type"].startswith("Basic"):
                assert card["card_type"].split(" — ")[0] in ("Basic Land", "Basic Snow Land")
                stats.num_basic_lands += 1
            elif card["rarity"] == "Common":
                stats.num_commons += 1
            elif card["rarity"] == "Uncommon":
                stats.num_uncommons += 1
            elif card["rarity"] == "Rare":
                stats.num_rares += 1
            else:
                raise ValueError(f"Unknown rarity: {card["rarity"]}")

    for stats in set_stats:
        print()
        print(stats.id)
        print(f"Common:      {stats.num_commons}")
        print(f"Uncommon:    {stats.num_uncommons}")
        print(f"Rares:       {stats.num_rares}")
        print(f"Basic Lands: {stats.num_basic_lands}")
        print(f"4:2:1 print: {stats.num_commons*4 + stats.num_uncommons*2 + stats.num_rares + stats.num_basic_lands*10}")

