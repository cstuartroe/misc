import json
import os.path

import bs4
import requests
import tqdm

from shared import Card, MY_SETS


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
            card.color = "L"

        else:
            cost_div = card_soup.find("span", {"class": "card-text-mana-cost"})
            if cost_div is None:
                print(f"Card '{card.title}' has no cost")
                symbols = []
            else:
                symbols = cost_div.find_all("abbr")

            colors = set()
            for symbol in symbols:
                sclass = symbol["class"]

                if sclass in (
                        ['card-symbol', 'card-symbol-0'],
                        ['card-symbol', 'card-symbol-1'],
                        ['card-symbol', 'card-symbol-2'],
                        ['card-symbol', 'card-symbol-3'],
                        ['card-symbol', 'card-symbol-4'],
                        ['card-symbol', 'card-symbol-5'],
                        ['card-symbol', 'card-symbol-6'],
                        ['card-symbol', 'card-symbol-7'],
                        ['card-symbol', 'card-symbol-8'],
                        ['card-symbol', 'card-symbol-9'],
                        ['card-symbol', 'card-symbol-10'],
                        ['card-symbol', 'card-symbol-11'],
                        ['card-symbol', 'card-symbol-12'],
                        ['card-symbol', 'card-symbol-15'],
                        ['card-symbol', 'card-symbol-X'],
                ):
                    pass

                elif sclass == ['card-symbol', 'card-symbol-B']:
                    colors.add("B")
                elif sclass == ['card-symbol', 'card-symbol-G']:
                    colors.add("G")
                elif sclass == ['card-symbol', 'card-symbol-R']:
                    colors.add("R")
                elif sclass == ['card-symbol', 'card-symbol-U']:
                    colors.add("U")
                elif sclass == ['card-symbol', 'card-symbol-W']:
                    colors.add("W")

                elif sclass == ['card-symbol', 'card-symbol-2B']:
                    colors.add("B")
                elif sclass == ['card-symbol', 'card-symbol-2G']:
                    colors.add("G")
                elif sclass == ['card-symbol', 'card-symbol-2R']:
                    colors.add("R")
                elif sclass == ['card-symbol', 'card-symbol-2U']:
                    colors.add("U")
                elif sclass == ['card-symbol', 'card-symbol-2W']:
                    colors.add("W")

                elif sclass == ['card-symbol', 'card-symbol-BP']:
                    colors.add("B")
                elif sclass == ['card-symbol', 'card-symbol-GP']:
                    colors.add("G")
                elif sclass == ['card-symbol', 'card-symbol-RP']:
                    colors.add("R")
                elif sclass == ['card-symbol', 'card-symbol-UP']:
                    colors.add("U")
                elif sclass == ['card-symbol', 'card-symbol-WP']:
                    colors.add("W")

                elif sclass == ['card-symbol', 'card-symbol-WU']:
                    colors.add("W")
                    colors.add("U")
                elif sclass == ['card-symbol', 'card-symbol-UB']:
                    colors.add("U")
                    colors.add("B")
                elif sclass == ['card-symbol', 'card-symbol-BR']:
                    colors.add("B")
                    colors.add("R")
                elif sclass == ['card-symbol', 'card-symbol-RG']:
                    colors.add("R")
                    colors.add("G")
                elif sclass == ['card-symbol', 'card-symbol-GW']:
                    colors.add("G")
                    colors.add("W")
                elif sclass == ['card-symbol', 'card-symbol-WU']:
                    colors.add("W")
                    colors.add("U")

                elif sclass == ['card-symbol', 'card-symbol-WB']:
                    colors.add("W")
                    colors.add("B")
                elif sclass == ['card-symbol', 'card-symbol-UR']:
                    colors.add("U")
                    colors.add("R")
                elif sclass == ['card-symbol', 'card-symbol-BG']:
                    colors.add("B")
                    colors.add("G")
                elif sclass == ['card-symbol', 'card-symbol-RW']:
                    colors.add("R")
                    colors.add("W")
                elif sclass == ['card-symbol', 'card-symbol-GU']:
                    colors.add("G")
                    colors.add("U")

                else:
                    raise ValueError(f"Unknown class on card {card.title}: {sclass}")

            card.color = ''.join(sorted(list(colors)))


def download_images(cards: list[Card]) -> None:
    for card in tqdm.tqdm(cards):
        res = requests.get(card.img_uri, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36"})
        with open(f"card_images/{card.id}.webp", "wb") as fh:
            fh.write(res.content)


if __name__ == "__main__":
    for set_id in MY_SETS:
        filepath = f"set_json/{set_id}.json"
        if os.path.exists(filepath):
            continue

        print(set_id)
        cards = scrape_gallery(set_id)
        get_additional_metadata(cards)
        with open(filepath, "w") as fh:
            json.dump([c.to_json() for c in cards], fh, indent=2)

        # download_images(cards)
