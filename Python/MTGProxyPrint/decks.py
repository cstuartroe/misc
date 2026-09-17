import math
import os
import random

from PIL import Image

from shared import MY_SETS, Card, load_set, COSTS
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

COLOR_SNOW_LANDS = {
    "B": "Snow-Covered Swamp",
    "G": "Snow-Covered Forest",
    "R": "Snow-Covered Mountain",
    "U": "Snow-Covered Island",
    "W": "Snow-Covered Plains",
}


MONOCOLOR_SETS = [
    "leb",
    "arn",
    "drk",
    "mir",
    "vis",
    "wth",
    "ody",
    "tor",
    "jud",
    "9ed",
    "csp",
    "tsp",
    "plc",
    "fut",
    "10e",
    "lrw",
    "mor",
]


BASIC_LAND_FALLBACKS = {
    "arn": "leb",
    "drk": "leb",
    "vis": "mir",
    "wth": "mir",
    "tor": "ody",
    "jud": "ody",
    "plc": "tsp",
    "fut": "tsp",
    "mor": "lrw",
}


def subsets_deck(prefix: str, set_colors: dict[tuple[str, str], int | None], basic_lands: dict[tuple[str, str], int | None], seed: int = SEED, skip_planeswalkers: bool = True) -> tuple[str, list[Card]]:
    random.seed(seed)

    title = prefix

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

        if count is None or count >= len(rarity_weighted):
            deck += rarity_weighted
            count = len(rarity_weighted)
        else:
            random.shuffle(rarity_weighted)
            deck += rarity_weighted[:count]

        title += f"_{set_id}-{color}-{count}"

        random.seed(deck[-1].title)

    deck_size_without_land = len(deck)

    for (set_id, land_name), count in basic_lands.items():
        if count is None:
            count = round(deck_size_without_land*.6/len(basic_lands))

        if set_id not in sets:
            sets[set_id] = load_set(set_id)

        land_cards = [card for card in sets[set_id] if card.title == land_name]

        if len(land_cards) == 0:
            raise ValueError(f"Set {set_id} has no basic lands")

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

    return "weighted_" + set_id, deck


def set_basic_lands(set_id: str, copies: int = 10) -> tuple[str, list[Card]]:
    set_cards = load_set(set_id)

    deck: list[Card] = []
    for card in set_cards:
        if card.card_type.startswith("Basic"):
            deck += [card]*copies

    return "basic_lands_" + set_id, deck


def deck_to_image(title: str, deck: list[Card]):
    image = Image.new("RGB", (CARD_WIDTH*10, CARD_HEIGHT*math.ceil(len(deck)/10)), "black")

    for i, card in enumerate(deck):
        x, y = i % 10, i // 10

        card_image = Image.open(f"card_images/{card.id}.webp")

        image.paste(card_image, (CARD_WIDTH*x, CARD_HEIGHT*y))

    image.save(f"decks/{title}.jpg")

    print(f"Wrote deck image {title}.jpg")


def mana_curve_image(title: str, deck: list[Card]):
    cmc_levels = {}
    max_creatures = 0
    max_noncreatures = 0

    for card in deck:
        if "Land" in card.card_type:
            continue

        if card.cmc not in cmc_levels:
            cmc_levels[card.cmc] = {"creatures": [], "noncreatures": []}

        if "Creature" in card.card_type:
            cmc_levels[card.cmc]["creatures"].append(card)
            max_creatures = max(max_creatures, len(cmc_levels[card.cmc]["creatures"]))
        else:
            cmc_levels[card.cmc]["noncreatures"].append(card)
            max_noncreatures = max(max_noncreatures, len(cmc_levels[card.cmc]["noncreatures"]))

    cmc_levels = sorted(list(cmc_levels.items()))

    width = int(CARD_WIDTH*(max_creatures + max_noncreatures + .5))
    height = CARD_HEIGHT*len(cmc_levels)
    image = Image.new("RGB", (width, height), "black")

    for i, (cmc, d) in enumerate(cmc_levels):
        for j, card in enumerate(d["creatures"]):
            x = CARD_WIDTH*(j + max_creatures - len(d["creatures"]))
            y = CARD_HEIGHT*i
            card_image = Image.open(f"card_images/{card.id}.webp")
            image.paste(card_image, (x, y))

        for j, card in enumerate(d["noncreatures"]):
            x = int(CARD_WIDTH*(max_creatures + .5 + j))
            y = CARD_HEIGHT*i
            card_image = Image.open(f"card_images/{card.id}.webp")
            image.paste(card_image, (x, y))


    image.save(f"decks/{title}_manacurve.jpg")

    print(f"Wrote deck image {title}_manacurve.jpg")


def deck_to_txt(title: str, deck: list[Card]):
    text = "Deck\n"
    for card in deck:
        text += f"1 {card.title} ({card.set_id.upper()}) {card.order}\n"

    with open(f"decks/{title}.txt", "w") as fh:
        fh.write(text)

    print(f"Wrote deck text {title}.txt")


def print_mana_curve(deck: list[Card]):
    cmcs = {}
    for card in deck:
        cmcs[card.cmc] = cmcs.get(card.cmc, 0) + 1

    for cmc, count in sorted(list(cmcs.items())):
        print(f"{cmc:>4}: {count:>2} ({round(100*count/len(deck)):>2}%)")


def print_release_stats(deck: list[Card]):
    set_counts = {}

    for card in deck:
        if "Basic" in card.card_type:
            continue

        set_counts[card.set_id] = set_counts.get(card.set_id, 0) + 1

    print("Number of cards per set:")
    for set_id, count in sorted(list(set_counts.items()), key=lambda x: MY_SETS.index(x[0])):
        print(f"{set_id}: {count:>3}")


def print_creature_stats(deck: list[Card]):
    creature_type_counts = {}
    for card in deck:
        if "Creature" in card.card_type:
            creature_type = card.card_type.split("—")[1].strip()
            creature_type_counts[creature_type] = creature_type_counts.get(creature_type, 0) + 1

    num_creatures = sum(creature_type_counts.values())
    print(f"{num_creatures} creatures.")
    print("Creature types:")
    for creature_type, count in sorted(list(creature_type_counts.items()), key=lambda x: -x[1]):
        print(f"{creature_type:>20}: {count:>2} ({round(count*100/num_creatures):>2}%)")

    creature_type_component_counts = {}
    for creature_type, count in creature_type_counts.items():
        components = creature_type.split(" ")
        for component in components:
            creature_type_component_counts[component] = creature_type_component_counts.get(component, 0) + count

    print("Creature type components:")
    for creature_type_component, count in sorted(list(creature_type_component_counts.items()), key=lambda x: -x[1]):
        print(f"{creature_type_component:>10}: {count:>2} ({round(count*100/num_creatures):>2}%)")


def generate_quick_decks():
    """60-card decks for quick play without doing any selection."""

    decks: list[tuple[str, list[Card]]] = []
    prefix = "quick"

    for color in "BGRUW":
        for set_id in MONOCOLOR_SETS:
            land_set_id = BASIC_LAND_FALLBACKS.get(set_id, set_id)
            land_names = COLOR_SNOW_LANDS if land_set_id == "csp" else COLOR_LANDS

            decks.append(subsets_deck(
                prefix,
                {(set_id, color): 38},
                {(land_set_id, land_names[color]): 22},
            ))

    for shadowmoor_color_pair in ["UW", "BU", "BR", "GR", "GW"]:
        decks.append(subsets_deck(
                prefix,
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
                prefix,
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
    prefix = "complete"

    for color in "BGRUW":
        for set_id in MONOCOLOR_SETS:
            land_set_id = BASIC_LAND_FALLBACKS.get(set_id, set_id)
            land_names = COLOR_SNOW_LANDS if land_set_id == "csp" else COLOR_LANDS

            decks.append(subsets_deck(
                prefix,
                {(set_id, color): None},
                {(land_set_id, land_names[color]): None},
            ))

    for shadowmoor_color_pair in ["UW", "BU", "BR", "GR", "GW"]:
        decks.append(subsets_deck(
                prefix,
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
                prefix,
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
    prefix = "colordraft"

    for color in "BGRUW":
        for set_id in MONOCOLOR_SETS:
            decks.append(subsets_deck(
                prefix,
                {(set_id, color): 54, (set_id, ""): 6},
                {},
            ))

    for shadowmoor_color_pair in ["UW", "BU", "BR", "GR", "GW"]:
        decks.append(subsets_deck(
                prefix,
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
                prefix,
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
                prefix,
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
                prefix,
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


def oneoff_lrwshm_ru_aggro():
    deck = []

    for set_id in ["lrw", "mor", "shm", "eve"]:
        set_cards = load_set(set_id)
        for card in set_cards:
            if "Basic Land" in card.card_type:
                continue

            if card.cost is None:  # Non-basic land:
                deck.append(card)
                continue

            all_costs_payable_by_ru = True
            for cost in card.cost:
                colors, _ = COSTS[cost]
                if len(colors) == 0 or "U" in colors or "R" in colors:
                    pass
                else:
                    all_costs_payable_by_ru = False

            if all_costs_payable_by_ru:
                deck.append(card)

    deck.sort(key=lambda card: -card.cmc)

    deck_to_txt("oneoff_lrwshm_ru_aggro", deck)

    # mana_curve_image("oneoff_lrwshm_ru_aggro", deck)


def oneoff_lrwshm_u_drawing():
    titles = [
        ("Advice from the Fae", True),
        ("Aethersnipe", True),
        ("Augury Adept", True),
        ("Banishing Knack", True),
        ("Biting Tether", True),
        ("Broken Ambitions", True),
        ("Captivating Glance", True),
        ("Cauldron of Souls", False),
        ("Cerulean Wisps", False),
        ("Clout of the Dominus", True),
        ("Cold-Eyed Selkie", False),
        ("Consign to Dream", True),
        ("Cryptic Command", True),
        ("Curse of Chains", True),
        ("Cursecatcher", True),
        ("Deathrender", False),
        ("Deepchannel Mentor", False),
        ("Dire Undercurrents", True),
        ("Disperse", True),
        ("Distant Melody", True),
        ("Diviner's Wand", True),
        ("Dolmen Gate", True),
        ("Dominus of Fealty", False),
        ("Door of Destinies", True),
        ("Dream Fracture", True),
        ("Ego Erasure", True),
        ("Faerie Swarm", True),
        ("Faerie Trickery", True),
        ("Fallowsage", True),
        ("Familiar's Ruse", True),
        ("Fathom Trawl", True),
        ("Flow of Ideas", True),
        ("Ghastlord of Fugue", True),
        ("Ghastly Discovery", True),
        ("Glen Elendra Archmage", True),
        ("Glen Elendra Liege", True),
        ("Glimmerdust Nap", True),
        ("Guile", False),
        ("Helm of the Ghastlord", True),
        ("Idle Thoughts", False),
        ("Illuminated Folio", True),
        ("Inkfathom Infiltrator", False),
        ("Inspired Sprite", True),
        ("Inundate", True),
        ("Jace Beleren", True),
        ("Leering Emblem", False),
        ("Memory Plunder", False),
        ("Merrow Commerce", False),
        ("Merrow Harbinger", True),
        ("Merrow Reejerey", True),
        ("Mind Spring", True),
        ("Mirrorweave", False),
        ("Mothdust Changeling", False),
        ("Mulldrifter", True),
        ("Murkfiend Liege", False),
        ("Negate", True),
        ("Nevermaker", False),
        ("Noggle Bandit", False),
        ("Nucklavee", False),
        ("Oona's Gatewarden", False),
        ("Oona's Grace", True),
        ("Overbeing of Myth", True),
        ("Ponder", True),
        ("Protective Bubble", True),
        ("Puca's Mischief", False),
        ("Puresight Merrow", True),
        ("Put Away", False),
        ("Ringskipper", True),
        ("Sage of Fables", True),
        ("Sage's Dousing", True),
        ("Scarscale Ritual", True),
        ("Scattering Stroke", True),
        ("Selkie Hedge-Mage", True),
        ("Shapesharer", True),
        ("Shell Skulkin", True),
        ("Sigil Tracer", True),
        ("Silvergill Adept", True),
        ("Silvergill Douser", True),
        ("Sinking Feeling", False),
        ("Somnomancer", True),
        ("Sower of Temptation", True),
        ("Spell Syphon", True),
        ("Steel of the Godhead", True),
        ("Stonybrook Angler", True),
        ("Stonybrook Banneret", True),
        ("Stream of Unconsciousness", True),
        ("Surgespanner", True),
        ("Sygg, River Cutthroat", True),
        ("Thieves' Fortune", True),
        ("Thought Reflection", True),
        ("Thoughtweft Gambit", False),
        ("Trip Noose", True),
        ("Turn to Mist", False),
        ("Wake Thrasher", True),
        ("Whirlpool Whelm", True),
        ("Wings of Velis Vel", True),
        ("Wistful Selkie", True),

        # Milling cards - may take or leave
        ("Drowner Initiate", False),
        ("Forced Fruition", False),
        ("Grimoire Thief", False),
        ("Ink Dissolver", False),
        ("Oona, Queen of the Fae", False),
        ("Sanity Grinding", False),
    ]

    sets = ["lrw", "mor", "shm", "eve"]

    lrwshm_cards_by_name = {}
    islands = []
    for set_id in sets:
        for card in load_set(set_id):
            lrwshm_cards_by_name[card.title] = card
            if card.title == "Island":
                islands.append(card)

    deck = []
    rejected = []
    for (title, include) in titles:
        card = lrwshm_cards_by_name[title]
        if include:
            deck.append(card)
        else:
            rejected.append(card)

    deck.sort(key=lambda card: (card.cmc, "Creature" in card.card_type, MY_SETS.index(card.set_id)))

    number_of_desired_islands = round(len(deck)*.65)

    print(f"Adding {number_of_desired_islands} islands to {len(deck)} non-land cards.")
    print(f"Rejected {len(rejected)} cards.")

    islands = (islands*math.ceil(number_of_desired_islands/len(islands)))[:number_of_desired_islands]
    islands.sort(key=lambda card: (MY_SETS.index(card.set_id), card.order))

    deck_with_islands = deck + islands

    title = "manual/beatshaun_LRWSHM_U_mono"
    deck_to_txt(title, deck_with_islands)
    mana_curve_image(title, deck)
    mana_curve_image(title + "_rejected", rejected)
    print_release_stats(deck)
    print_creature_stats(deck)


def wither_me_worries():
    titles = [
        (1, "Cinderhaze Wretch"),
        (1, "Needle Specter"),
        (1, "Blowfly Infestation"),
        (1, "Corrosive Mentor"),
        (1, "Puppeteer Clique"),
        (1, "Fate Transfer"),
        (1, "Restless Apparition"),
        (1, "Voracious Hatchling"),
        (1, "Quillspike"),
        (1, "Rendclaw Trow"),
        (1, "Cauldron Haze"),
        (1, "Austere Command"),
        (1, "Ajani Goldmane"),
        (1, "Blight Sickle"),
        (1, "Chainbreaker"),
        (1, "Gnarled Effigy"),
        (1, "Dusk Urchins"),
        (1, "Crumbling Ashes"),
        (1, "Eyeblight's Ending"),
        (1, "Necroskitter"),
        (1, "Canker Abomination"),
        (1, "Flourishing Defenses"),
        (1, "Harvest Gwyllion"),
        (1, "Soul Snuffers"),
        (1, "Incremental Blight"),
        (1, "Deity of Scars"),
        (1, "Wickerbough Elder"),
        (1, "Heartmender"),
        (1, "Creakwood Liege"),
        (1, "Devoted Druid"),
        (1, "Torture"),
        (1, "Nettlevine Blight"),
        (1, "Everlasting Torment"),
        (1, "Sickle Ripper"),
        (1, "Scar"),
        (1, "Oona's Gatewarden"),
        (12, "Swamp"),
        (1, "Twilight Mire"),
        (1, "Wooded Bastion"),
        (1, "Windbrisk Heights"),
        (1, "Vivid Meadow"),
        (5, "Plains"),
        (1, "Reflecting Pool"),
        (1, "Murmuring Bosk"),
        (1, "Shimmering Grotto"),
    ]

    sets = ["lrw", "mor", "shm", "eve"]

    lrwshm_cards_by_name = {}
    islands = []
    for set_id in sets:
        for card in load_set(set_id):
            lrwshm_cards_by_name[card.title] = card

    deck = []
    for (count, title) in titles:
        card = lrwshm_cards_by_name[title]
        deck += [card]*count

    deck.sort(key=lambda card: (card.cmc, "Creature" in card.card_type, MY_SETS.index(card.set_id)))

    title = "manual/wither_me_worries"
    deck_to_txt(title, deck)
    mana_curve_image(title, deck)
    print_release_stats(deck)
    print_creature_stats(deck)


if __name__ == "__main__":
    for file in os.listdir(path="decks"):
        if file.endswith(".txt") or file.endswith("png"):
            os.unlink(f"decks/{file}")

    generate_quick_decks()
    generate_complete_decks()
    generate_drafting_decks()
    generate_weighted_sets()
    my_cards()
    # oneoff_lrwshm_ru_aggro()
    oneoff_lrwshm_u_drawing()
    wither_me_worries()
