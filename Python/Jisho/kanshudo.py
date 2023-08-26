import os
import re
from dataclasses import dataclass
import requests
import bs4
from bs4 import BeautifulSoup as bs

HOST = "https://www.kanshudo.com"
STARTING_PAGE = HOST + "/collections/wikipedia_jlpt"
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"

HEADERS = {
    "User-Agent": USER_AGENT,
}


@dataclass
class Word:
    spelling: str
    pronunciation: str
    accent_patterns: list[str]
    definition: str

    def __str__(self):
        return f"{self.spelling} <{self.pronunciation}> {self.accent_patterns} \"{self.definition}\""


@dataclass
class Level:
    level: int
    words: list[Word]


def load_word(word_div: bs4.PageElement) -> Word:
    spelling_box: bs4.PageElement = word_div.a
    spelling = ""
    pronunciation = ""
    for child in spelling_box:
        if isinstance(child, bs4.NavigableString):
            spelling += child
            pronunciation += child
        elif isinstance(child, bs4.PageElement):
            spelling += child.find("div", {"class": "f_kanji"}).text
            pronunciation += child.find("div", {"class": "furigana"}).text
        else:
            raise ValueError("Unknown child type")

    accent_patterns: list[str] = []

    for svg in word_div.find_all("svg"):
        texts = svg.find_all("text")
        pronunciation_check = ''.join([t.text for t in texts[:-1]])
        assert pronunciation == pronunciation_check

        accent = texts[-1].text.strip()

        try:
            int(accent)
        except ValueError as e:
            print(e)
            print(spelling, pronunciation)

        accent_patterns.append(accent)

    accent_patterns.sort()

    definitions = word_div.find("div", {"class": "jukugo_reading"}).div
    first_definition = definitions.find("div", {"class": "vm"})
    definition_div = first_definition or definitions
    definition = ""
    for child in definition_div.children:
        if isinstance(child, bs4.NavigableString):
            stripped = child.strip()

            if len(stripped) == 0:
                continue

            if len(definition) > 0:
                print("Warning: multiple definition")
                print(spelling, pronunciation)
                print(definition, stripped)

            definition += stripped

    if len(definition) == 0:
        print("Warning: empty definition")
        print(spelling, pronunciation)
        print(list(definitions.children))

    out = Word(spelling, pronunciation, accent_patterns, definition)
    # print(out)
    return out


def load_vocab_link(vocab_link: str) -> list[Word]:
    print(vocab_link)
    res = requests.get(vocab_link, headers=HEADERS)
    soup = bs(res.text, features="html.parser")

    word_divs = soup.find_all("div", {"class": "jukugorow first last"})
    return [
        load_word(word_div)
        for word_div in word_divs
    ]


def load_level(level_div: bs4.PageElement) -> Level:
    m = re.fullmatch(r"Wikipedia JLPT N(\d) Vocab \((\d+) words\)", level_div.h4.text)
    level = int(m.group(1))
    num_words = int(m.group(2))

    words: list[Word] = []
    for link in level_div.find_all("a"):
        vocab_link = HOST + link["href"]
        words += load_vocab_link(vocab_link)

    if len(words) != num_words:
        print(f"Level supposed to have {num_words} words, actually has {len(words)}")

    return Level(level, words)


def get_levels() -> list[Level]:
    res = requests.get(STARTING_PAGE, headers=HEADERS)
    soup = bs(res.text, features="html.parser")
    level_divs = soup.find_all("div", {"class": "infopanel"})

    return [
        load_level(level_div)
        for level_div in level_divs
    ]


def export_level_for_anki(level: Level):
    content = ""
    for word in level.words:
        pronunciation = word.pronunciation
        if word.pronunciation == word.spelling:
            pronunciation = ""
        content += f"{word.spelling:<10};{pronunciation:<10};{','.join(word.accent_patterns):<6};{word.definition.replace(';', ',')};\n"

    with open(f"anki/N{level.level}.txt", "w") as fh:
        fh.write(content)


if __name__ == "__main__":
    levels = get_levels()

    accent_pattern_frequencies = {}

    for level in levels:
        for word in level.words:
            tup = tuple(word.accent_patterns)
            accent_pattern_frequencies[tup] = accent_pattern_frequencies.get(tup, 0) + 1

    pairs = sorted(list(accent_pattern_frequencies.items()), key=lambda p: p[1])

    for patterns, count in pairs:
        print(patterns, count)

    os.makedirs("anki", exist_ok=True)

    for level in levels:
        export_level_for_anki(level)
