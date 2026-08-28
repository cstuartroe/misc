import math
import random

from PIL import Image

from shared import MY_SETS, Card, load_set
from my_cards import load_my_cards


CARD_WIDTH = 488
CARD_HEIGHT = 680


SEED = 2008


COLOR_LANDS = {
    "B": "Swamp",
    "G": "Forest",
    "R": "Mountain",
    "U": "Island",
    "W": "Plains",
}


def subsets_deck(set_colors: dict[tuple[str, str], int | None], basic_lands: dict[tuple[str, str], int | None], seed: int = SEED, skip_planeswalkers: bool = True) -> tuple[str, list[Card]]:
    random.seed(seed)

    title = str(seed).zfill(4)

    sets = {}
    deck: list[Card] = []

    for (set_id, color), count in set_colors.items():
        if set_id not in sets:
            sets[set_id] = load_set(set_id)

        cards_of_color = [card for card in sets[set_id] if card.color == color]
        rarity_weighted = []
        for card in cards_of_color:
            if "Planeswalker" in card.card_type and skip_planeswalkers:
                pass
            elif card.rarity == "Common":
                rarity_weighted += [card, card, card, card]
            elif card.rarity == "Uncommon":
                rarity_weighted += [card, card]
            elif card.rarity == "Rare":
                rarity_weighted.append(card)
            else:
                raise ValueError

        random.shuffle(rarity_weighted)

        if count is None:
            count = len(rarity_weighted)

        deck += rarity_weighted[:count]
        title += f"_{set_id}-{color}-{count}"

        random.seed(deck[-1].title)

    for (set_id, land_name), count in basic_lands.items():
        if count is None:
            count = round(len(deck)*.58/len(basic_lands))

        if set_id not in sets:
            sets[set_id] = load_set(set_id)

        land_cards = [card for card in sets[set_id] if card.title == land_name]
        multiples = []
        for _ in range(math.ceil(count/len(land_cards))):
            multiples += land_cards

        random.shuffle(multiples)
        deck += multiples[:count]

        title += f"_{set_id}-{land_name}-{count}"

    deck.sort(key=lambda card: (MY_SETS.index(card.set_id), card.order))

    return title, deck


def weighted_set(set_id: str, include_basic_lands: bool = False) -> tuple[str, list[Card]]:
    set_cards = load_set(set_id)

    deck: list[Card] = []
    for card in set_cards:
        if card.card_type.startswith("Basic") and not include_basic_lands:
            pass
        elif card.rarity == "Common":
            deck += [card, card, card, card]
        elif card.rarity == "Uncommon":
            deck += [card, card]
        else:
            deck.append(card)

    return set_id + "_weighted", deck


def set_basic_lands(set_id: str, copies: int = 10) -> tuple[str, list[Card]]:
    set_cards = load_set(set_id)

    deck: list[Card] = []
    for card in set_cards:
        if card.card_type.startswith("Basic"):
            deck += [card]*copies

    return set_id + "_basic_lands", deck


def deck_to_image(title: str, deck: list[Card]):
    image = Image.new("RGB", (CARD_WIDTH*10, CARD_HEIGHT*math.ceil(len(deck)/10)), "black")

    for i, card in enumerate(deck):
        x, y = i % 10, i // 10

        card_image = Image.open(f"card_images/{card.id}.webp")

        image.paste(card_image, (CARD_WIDTH*x, CARD_HEIGHT*y))

    image.save(f"decks/{title}.png")

    print(f"Wrote deck image {title}.png")


def deck_to_txt(title: str, deck: list[Card]):
    text = "Deck\n"
    for card in deck:
        text += f"1 {card.title} ({card.set_id.upper()}) {card.order}\n"

    with open(f"decks/{title}.txt", "w") as fh:
        fh.write(text)

    print(f"Wrote deck text {title}.txt")


def generate_quick_decks():
    """60-card decks for quick play without doing any selection."""

    decks: list[tuple[str, list[Card]]] = []

    for color in "BGRUW":
        decks.append(subsets_deck(
            {("10e", color): 38},
            {("10e", COLOR_LANDS[color]): 22},
        ))
        decks.append(subsets_deck(
            {("lrw", color): 38},
            {("lrw", COLOR_LANDS[color]): 22},
        ))

    for shadowmoor_color_pair in ["UW", "BU", "BR", "GR", "GW"]:
        decks.append(subsets_deck(
            {
                ("shm", shadowmoor_color_pair[0]): 10,
                ("shm", shadowmoor_color_pair[1]): 10,
                ("shm", shadowmoor_color_pair): 18,
            },
            {
                ("shm", COLOR_LANDS[shadowmoor_color_pair[0]]): 11,
                ("shm", COLOR_LANDS[shadowmoor_color_pair[1]]): 11,
            },
        ))

    for eventide_color_pair in ["BW", "RU", "BG", "RW", "GU"]:
        decks.append(subsets_deck(
            {
                ("eve", eventide_color_pair[0]): 10,
                ("eve", eventide_color_pair[1]): 10,
                ("eve", eventide_color_pair): 18,
            },
            {
                ("shm", COLOR_LANDS[eventide_color_pair[0]]): 11,
                ("shm", COLOR_LANDS[eventide_color_pair[1]]): 11,
            },
        ))

    for title, deck in decks:
        # deck_to_image(title, deck)
        deck_to_txt(title, deck)


def generate_complete_decks():
    """Decks containing all cards of given color(s) in sets."""

    decks: list[tuple[str, list[Card]]] = []

    for color in "BGRUW":
        decks.append(subsets_deck(
            {("10e", color): None},
            {("10e", COLOR_LANDS[color]): None},
        ))
        decks.append(subsets_deck(
            {("lrw", color): None},
            {("lrw", COLOR_LANDS[color]): None},
        ))

    for shadowmoor_color_pair in ["UW", "BU", "BR", "GR", "GW"]:
        decks.append(subsets_deck(
            {
                ("shm", shadowmoor_color_pair[0]): None,
                ("shm", shadowmoor_color_pair[1]): None,
                ("shm", shadowmoor_color_pair): None,
            },
            {
                ("shm", COLOR_LANDS[shadowmoor_color_pair[0]]): None,
                ("shm", COLOR_LANDS[shadowmoor_color_pair[1]]): None,
            },
        ))

    for eventide_color_pair in ["BW", "RU", "BG", "RW", "GU"]:
        decks.append(subsets_deck(
            {
                ("eve", eventide_color_pair[0]): None,
                ("eve", eventide_color_pair[1]): None,
                ("eve", eventide_color_pair): None,
            },
            {
                ("shm", COLOR_LANDS[eventide_color_pair[0]]): None,
                ("shm", COLOR_LANDS[eventide_color_pair[1]]): None,
            },
        ))

    for title, deck in decks:
        # deck_to_image(title, deck)
        deck_to_txt(title, deck)


def generate_drafting_decks():
    """60-card decks with no basic lands, with the intention that drafters will build a deck out of the drafted cards."""

    decks: list[tuple[str, list[Card]]] = []

    for color in "BGRUW":
        decks.append(subsets_deck(
            {("10e", color): 54, ("10e", ""): 6},
            {},
        ))
        decks.append(subsets_deck(
            {("lrw", color): 54, ("lrw", ""): 6},
            {},
        ))

    for shadowmoor_color_pair in ["UW", "BU", "BR", "GR", "GW"]:
        decks.append(subsets_deck(
            {
                ("shm", shadowmoor_color_pair[0]): 10,
                ("eve", shadowmoor_color_pair[0]): 10,
                ("shm", shadowmoor_color_pair[1]): 10,
                ("eve", shadowmoor_color_pair[1]): 10,
                ("shm", shadowmoor_color_pair): 20,
            },
            {},
        ))
        decks.append(subsets_deck(
            {
                ("shm", shadowmoor_color_pair[0]): 15,
                ("shm", shadowmoor_color_pair[1]): 15,
                ("shm", shadowmoor_color_pair): 24,
                ("shm", ""): 6,
            },
            {},
        ))

    for eventide_color_pair in ["BW", "RU", "BG", "RW", "GU"]:
        decks.append(subsets_deck(
            {
                ("shm", eventide_color_pair[0]): 10,
                ("eve", eventide_color_pair[0]): 10,
                ("shm", eventide_color_pair[1]): 10,
                ("eve", eventide_color_pair[1]): 10,
                ("eve", eventide_color_pair): 20,
            },
            {}
        ))
        decks.append(subsets_deck(
            {
                ("eve", eventide_color_pair[0]): 15,
                ("eve", eventide_color_pair[1]): 15,
                ("eve", eventide_color_pair): 24,
                ("eve", ""): 6,
            },
            {},
        ))

    for title, deck in decks:
        # deck_to_image(title, deck)
        deck_to_txt(title, deck)


def generate_weighted_sets():
    """4-2-1 weighted drafting cubes for all sets."""

    for set_id in MY_SETS:
        title, deck = weighted_set(set_id)
        deck_to_txt(title, deck)
        # deck_to_image(title, deck)

        title, deck = set_basic_lands(set_id)
        if deck:
            deck_to_txt(title, deck)
            # deck_to_image(title, deck)


def my_cards():
    my_cards = load_my_cards()
    deck_to_txt("my_cards", my_cards)
    # deck_to_image("my_cards", my_cards)


if __name__ == "__main__":
    generate_quick_decks()
    generate_complete_decks()
    generate_drafting_decks()
    generate_weighted_sets()
    my_cards()
