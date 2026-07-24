import json

from fpdf import fpdf
import tqdm

import download


MARGIN_LEFT = 10
MARGIN_TOP = 10
CARD_WIDTH = 63
CARD_HEIGHT = 88


if __name__ == "__main__":
    for set_id in download.MY_SETS:
        print(set_id)

        with open(f"set_json/{set_id}.json", "r") as fh:
            set_json = json.load(fh)

        printed_cards = []
        for card in set_json:
            if card["card_type"].startswith("Basic"):
                multiple = 10
            elif card["rarity"] == "Common":
                multiple = 4
            elif card["rarity"] == "Uncommon":
                multiple = 2
            elif card["rarity"] == "Rare":
                multiple = 1
            else:
                raise ValueError

            for _ in range(multiple):
                printed_cards.append(card["id"])

        pdf = fpdf.FPDF(
            orientation=fpdf.PageOrientation.PORTRAIT,
            unit="mm",
            format="A4",
        )

        for i, card_id in tqdm.tqdm(list(enumerate(printed_cards))):
            if i % 9 == 0:
                pdf.add_page()

            x = MARGIN_LEFT + CARD_WIDTH*(i%3)
            y = MARGIN_TOP + CARD_HEIGHT*((i%9)//3)

            pdf.image(f"card_images/{card_id}.webp", x=x, y=y, w=CARD_WIDTH, h=CARD_HEIGHT)

        pdf.output(f"pdfs/{set_id}.pdf")


