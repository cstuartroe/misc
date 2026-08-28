import dataclasses

from shared import Card, MY_SETS, load_set
from my_cards import load_my_cards


card_names_to_sets = {}


@dataclasses.dataclass
class SetStats:
    id: str = ""
    num_cards: int = 0
    num_commons: int = 0
    num_uncommons: int = 0
    num_rares: int = 0
    num_mythic_rares: int = 0
    num_basic_lands: int = 0
    color_counts: dict = None


def get_stats(cards: list[Card]) -> SetStats:
    stats = SetStats(color_counts={})

    for card in cards:
        stats.num_cards += 1

        if card.card_type.startswith("Basic"):
            assert card.card_type.split(" — ")[0] in ("Basic Land", "Basic Snow Land")
            stats.num_basic_lands += 1
        elif card.rarity == "Common":
            stats.num_commons += 1
        elif card.rarity == "Uncommon":
            stats.num_uncommons += 1
        elif card.rarity == "Rare":
            stats.num_rares += 1
        elif card.rarity == "Mythic Rare":
            stats.num_mythic_rares += 1
        else:
            raise ValueError(f"Unknown rarity: {card.rarity}")

        stats.color_counts[card.color] = stats.color_counts.get(card.color, 0) + 1

    return stats


def print_stats(stats: SetStats):
    print(f"{stats.id} - {stats.num_cards} cards")
    print(f"Common:       {stats.num_commons}")
    print(f"Uncommon:     {stats.num_uncommons}")
    print(f"Rares:        {stats.num_rares}")
    if stats.num_mythic_rares > 0:
        print(f"Mythic Rares: {stats.num_rares}")
    print(f"Basic Lands:  {stats.num_basic_lands}")
    print(f"4:2:1 print:  {stats.num_commons * 4 + stats.num_uncommons * 2 + stats.num_rares}")
    print("Color counts:")
    for color in stats.color_counts:
        print(f"  {color:<2}: {stats.color_counts[color]:>2}")
    print()


if __name__ == "__main__":
    set_stats = []

    for set_id in MY_SETS:
        cards: list[Card] = load_set(set_id)
        stats = get_stats(cards)
        stats.id = set_id
        set_stats.append(stats)

    for stats in set_stats:
        print_stats(stats)

    print()
    print()

    card_names_to_sets.clear()

    my_cards = load_my_cards()
    stats = get_stats(my_cards)
    stats.id = "my_cards"
    print_stats(stats)

    for set_id in MY_SETS:
        cards = [card for card in my_cards if card.set_id == set_id]
        stats = get_stats(cards)
        stats.id = f"my_cards:{set_id}"
        print_stats(stats)
