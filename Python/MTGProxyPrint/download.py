import json
import os.path
import re

import bs4
import requests
import tqdm

from shared import Card, MY_SETS, COSTS


def scrape_gallery(set_id: str) -> list[Card]:
    gallery_res = requests.get(f"https://scryfall.com/sets/{set_id}")
    gallery_soup = bs4.BeautifulSoup(gallery_res.content, features="html.parser")

    cards = []

    for header in gallery_soup.find_all("h2", {"class": "card-grid-header"}):
        header_text = header.text.strip()
        section_name = header_text.split(" •\n")[0]
        if section_name != "In Boosters":
            print(f"Skipping {repr(section_name)}")
            continue

        card_grid = header.next_sibling.next_sibling

        assert card_grid.name == "div"
        assert card_grid["class"] == ["card-grid"]
        assert card_grid.div["class"] == ["card-grid-inner"]

        for card_grid_item in card_grid.div.children:
            if card_grid_item.name is None:
                continue

            assert card_grid_item.name == "div"

            if card_grid_item["class"] == ["card-grid-item", "flexbox-spacer"]:
                continue

            assert card_grid_item["class"] in (["card-grid-item"], ["card-grid-item", "wide"])

            cards.append(Card(
                id=card_grid_item["data-card-id"],
                title=card_grid_item.a.span.text.strip(),
                set_id=set_id,
                order=len(cards) + 1,
                scryfall_uri=card_grid_item.a["href"],
                img_uri=card_grid_item.img["src"].split("?")[0],
            ))

    return cards


def get_additional_metadata(cards: list[Card]) -> None:
    for card in tqdm.tqdm(cards):
        card_res = requests.get(card.scryfall_uri)
        card_soup = bs4.BeautifulSoup(card_res.content, features="html.parser")

        card.card_type = card_soup.find("p", {"class": "card-text-type-line"}).text.strip()
        card.rarity = card_soup.find("span", {"class": "prints-current-set-details"}).text.split("·")[1].strip()

        if "Land" in card.card_type:
            card.cost = None

        else:
            cost_div = card_soup.find("span", {"class": "card-text-mana-cost"})
            if cost_div is None:
                print(f"Card '{card.title}' has no cost")
                symbols = []
            else:
                symbols = cost_div.find_all("abbr")

            card.cost = []
            for symbol in symbols:
                sclass = symbol["class"]

                assert len(sclass) == 2
                assert sclass[0] == "card-symbol"
                m = re.fullmatch("card-symbol-([0-9BGRUWXP]+)", sclass[1])
                assert m is not None

                cost = m.group(1)

                if cost not in COSTS:
                    raise ValueError(f"Unknown class on card {card.title}: {sclass}")

                card.cost.append(cost)


def download_images(cards: list[Card]) -> None:
    for card in tqdm.tqdm(cards):
        res = requests.get(card.img_uri, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36"})
        with open(f"card_images/{card.id}.webp", "wb") as fh:
            fh.write(res.content)


if __name__ == "__main__":
    for set_id in MY_SETS:
        filepath = f"set_json/{set_id}.json"
        # if os.path.exists(filepath):
        #     continue

        print(set_id)
        cards = scrape_gallery(set_id)
        get_additional_metadata(cards)
        with open(filepath, "w") as fh:
            json.dump([c.to_json() for c in cards], fh, indent=2)

        download_images(cards)
