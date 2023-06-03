import json
import os
import time
from dataclasses import dataclass
import re
import bs4
from bs4 import BeautifulSoup as bs
import requests

@dataclass
class Form:
    form: str
    reading: str
    parse_method: str

    def reading_str(self):
        return f"{self.form} 【{self.reading}】"

    def json(self):
        return {
            "form": self.form,
            "reading": self.reading,
            "parse_method": self.parse_method,
        }

@dataclass
class Definition:
    tags: str
    meaning: str

    def json(self):
        return {
            "tags": self.tags,
            "meaning": self.meaning,
        }


@dataclass
class VocabularyItem:
    main_form: Form
    other_forms: list[Form]
    level: int
    definitions: list[Definition]

    def json(self):
        return {
            "main_form": self.main_form.json(),
            "other_forms": [f.json() for f in self.other_forms],
            "level": self.level,
            "definitions": [d.json() for d in self.definitions],
        }


def parse_main_form(main_form_div: bs4.PageElement) -> Form:
    furigana_span = main_form_div.find("span", {"class": "furigana"})

    ruby = furigana_span.find("ruby")
    if ruby:
        form_element, reading_element = ruby.children
        return Form(form=form_element.text, reading=reading_element.text, parse_method="ruby")

    form_furigana = [e.text.strip() for e in furigana_span.children]
    assert form_furigana[0] == ""
    assert form_furigana[-1] == ""
    form_furigana = form_furigana[1:-1]

    form_characters = []
    for e in main_form_div.find("span", {"class": "text"}).children:
        if type(e) is bs4.NavigableString:
            form_characters += [*e.strip()]
        else:
            form_characters.append(e.text)


    form = ""
    reading = ""
    parse_method = "normal"

    for c, furigana in zip(form_characters, form_furigana):
        form += c
        reading += furigana or c

    if len(form_furigana) != len(form_characters):
        if len(form_furigana) > len(form_characters):
            raise ValueError

        parse_method = "unseparated_furigana"
        form += ''.join(form_characters[len(form_furigana):])

        print("Unseparated furigana")
        print(main_form_div)
        print(form_characters)
        print(form_furigana)
        print(form)
        print(reading)

    return Form(form=form, reading=reading, parse_method=parse_method)


def parse_level(status_div: bs4.PageElement) -> int:
    spans = status_div.find_all("span")
    for span in spans:
        m = re.fullmatch(r"JLPT N(\d)", span.text)
        if m:
            return int(m.group(1))

    return 0


def parse_other_forms(s: str) -> list[Form]:
    forms = []

    for pair in s.split('、'):
        if pair[-1] == '】':
            form, reading = pair[:-1].split('【')
            forms.append(Form(form=form, reading=reading, parse_method="other_forms_kanji"))
        else:
            forms.append(Form(form=pair, reading=pair, parse_method="other_forms_kana"))

    return forms


def parse_meanings(meaning_div) -> tuple[list[Definition], list[Form]]:
    definitions: list[Definition] = []
    forms: list[Form] = []

    current_tag = None
    for div in meaning_div.children:
        div_class = div["class"][0]
        if div_class == "meaning-tags":
            current_tag = div.text

        elif div_class == "meaning-wrapper":
            if current_tag == "Notes":
                pass

            elif current_tag == "Other forms":
                forms = parse_other_forms(div.text)

            else:
                definitions.append(Definition(
                    tags=current_tag,
                    meaning=div.find("span", {"class": "meaning-meaning"}).text,
                ))

        else:
            raise ValueError(f"Unrecognized class: {div['class']}")

    return definitions, forms


def parse_vocab(vocab_soup: bs4.PageElement) -> VocabularyItem:
    main_form = parse_main_form(vocab_soup.find("div", {"class": "concept_light-representation"}))
    level = parse_level(vocab_soup.find("div", {"class": "concept_light-status"}))
    definitions, other_forms = parse_meanings(vocab_soup.find("div", {"class", "meanings-wrapper"}))

    return VocabularyItem(
        main_form=main_form,
        other_forms=other_forms,
        level=level,
        definitions=definitions,
    )


def get_vocab_page(level: int, page: int):
    res = requests.get(f"https://jisho.org/search/%20%23words%20%23jlpt-n{level}?page={page}")

    os.makedirs("pages/", exist_ok=True)
    with open(f"pages/{page}.html", "w") as fh:
        fh.write(res.text)

    soup = bs(res.text, features="html.parser")

    for clearfix in soup.find_all("div", {"class": "concept_light clearfix"}):
        yield parse_vocab(clearfix)


def get_vocab_page_attempt(level: int, page: int, retries: int = 3):
    for i in range(retries, 0, -1):
        page_items = list(get_vocab_page(level, page))
        if page_items:
            if i < retries:
                print(f"Page came back from the dead: {level} {page}")
            return page_items

        if i > 1:
            time.sleep(20)
            print(f"Retrying {level} {page}...")
        else:
            print("Fetched nothing")

    return []


def get_vocab_items(level: int) -> list[VocabularyItem]:
    items = []
    page = 1

    while True:
        print(page)
        page_items = get_vocab_page_attempt(level, page)
        if page_items:
            items += page_items
            page += 1
        else:
            break

    return items


if __name__ == "__main__":
    dictionary = {}
    for level in range(1, 6):
        for item in get_vocab_items(level):
            key = item.main_form.reading_str()
            if key in dictionary:
                if dictionary[key] != item.json():
                    print(f"Duplicate entry: {key}")
                    print(json.dumps(dictionary[key], indent=2, sort_keys=True, ensure_ascii=False))
                    print(json.dumps(item.json(), indent=2, sort_keys=True, ensure_ascii=False))

                    if len(item.definitions) > len(dictionary[key]["definitions"]):
                        print("Replacing")
                        dictionary[key] = item.json()
            else:
                dictionary[key] = item.json()

    print(f"Dictionary size: {len(dictionary)}")

    level_counts = {}
    for item in dictionary.values():
        level_counts[item["level"]] = level_counts.get(item["level"], 0) + 1
    print(level_counts)

    with open("jisho_vocab.json", "w") as fh:
        json.dump(dictionary, fh, sort_keys=True, indent=2, ensure_ascii=False)
