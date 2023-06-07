import requests
import json
from dataclasses import dataclass, asdict
import re


INVENTORY_REGEX = r'<a class="Contribution" href="https://phoible.org/inventories/view/(\d+)" title="(.+)">(.+)</a>'
LANGUAGE_REGEX = r'<a class="Language" href="https://phoible.org/languages/(.+)" title="(.+)">(.+)</a>'
SEGMENT_REGEX = r'<a class="Parameter" href="https://phoible.org/parameters/([A-Z0-9]+)" title="(.+)">(.+)</a>'


@dataclass
class Segment:
    stype: str
    id: str
    ipa: str
    marginal: str
    allophones: list[str]


@dataclass
class Inventory:
    id: int
    title: str
    languageId: str
    languageName: str
    vowels: list[Segment] = None
    consonants: list[Segment] = None
    tones: list[Segment] = None

    @classmethod
    def from_dict(cls, d: dict):
        kwargs = {**d}
        for stype in ("vowels", "consonants", "tones"):
            kwargs[stype] = [
                Segment(**s)
                for s in d[stype]
            ]
        return cls(**kwargs)

    def load_segments(self, num_vowels: int, num_consonants: int, num_tones: int):
        self.vowels, self.consonants, self.tones = [], [], []

        rows = []
        page = 0

        while True:
            res = requests.get(
                "https://phoible.org/values",
                headers={
                    "X-Requested-With": 'XMLHttpRequest',
                },
                params={
                    "contribution": self.id,
                    "sEcho": '1',
                    "iDisplayStart": page*1000,
                    "iDisplayLength": 1000,
                }
            )

            data = json.loads(res.text)
            pageRows = data["aaData"]

            if pageRows:
                if page > 0:
                    raise ValueError
                rows += pageRows
                page += 1
            else:
                break

        for row in rows:
            segment_type, segment_html, marginal, allophones, _ = row
            id, ipa, ipa_check = re.fullmatch(SEGMENT_REGEX, segment_html).groups()
            allophones = allophones.split()

            assert ipa == ipa_check
            assert marginal in ("", "False", "True")

            segment = Segment(
                stype=segment_type,
                id=id,
                ipa=ipa,
                marginal=marginal,
                allophones=allophones,
            )

            if segment_type == "vowel":
                self.vowels.append(segment)
            elif segment_type == "consonant":
                self.consonants.append(segment)
            elif segment_type == "tone":
                self.tones.append(segment)
            else:
                raise ValueError(f"Unknown segment type: {segment_type}")

        assert len(self.vowels) == num_vowels
        assert len(self.consonants) == num_consonants
        assert len(self.tones) == num_tones


def get_inventories():
    rows = []
    page = 0

    while True:
        res = requests.get(
            "https://phoible.org/inventories",
            headers={
                "X-Requested-With": 'XMLHttpRequest',
            },
            params={
                "sEcho": "",
                "iDisplayStart": page * 1000,
                "iDisplayLength": 1000,
            }
        )

        data = json.loads(res.text)

        pageRows = data["aaData"]
        if pageRows:
            rows += pageRows
            page += 1
        else:
            break

    for (inventoryHTML, langHTML, num_segments, num_vowels, num_consonants, num_tones, _, _) in rows:
        id, title, titleCheck = re.fullmatch(INVENTORY_REGEX, inventoryHTML).groups()
        assert title == titleCheck

        languageId, languageName, languageNameCheck = re.fullmatch(LANGUAGE_REGEX, langHTML).groups()
        assert languageName == languageNameCheck

        if num_tones == "":
            num_tones = 0
        assert num_segments == (num_vowels + num_consonants + num_tones)

        inv = Inventory(
            id=id,
            title=title,
            languageId=languageId,
            languageName=languageName,
        )
        inv.load_segments(
            num_vowels=num_vowels,
            num_consonants=num_consonants,
            num_tones=num_tones,
        )
        print((inv.id, inv.title))
        yield inv


if __name__ == "__main__":
    with open("inventories.json", "w") as fh:
        json.dump(
            [
                asdict(inv)
                for inv in get_inventories()
            ],
            fh,
            indent=2,
            sort_keys=False,
            ensure_ascii=False,
        )
