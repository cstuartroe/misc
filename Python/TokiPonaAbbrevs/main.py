import re

ROOTS: list[str] = [
    "a",
    "akesi",
    "ala",
    "alasa",
    "ale",
    "ali",
    "anpa",
    "ante",
    "anu",
    "awen",
    "e",
    "en",
    "esun",
    "ijo",
    "ike",
    "ilo",
    "insa",
    "jaki",
    "jan",
    "jelo",
    "jo",
    "kala",
    "kalama",
    "kama",
    "kasi",
    "ken",
    "kepeken",
    "kili",
    "kin",
    "kipisi",
    "kiwen",
    "ko",
    "kon",
    "kule",
    "kulupu",
    "kute",
    "la",
    "lape",
    "laso",
    "lawa",
    "len",
    "lete",
    "li",
    "lili",
    "linja",
    "lipu",
    "loje",
    "lon",
    "luka",
    "lukin",
    "lupa",
    "ma",
    "mama",
    "mani",
    "meli",
    "mi",
    "mije",
    "moku",
    "moli",
    "monsi",
    "mu",
    "mun",
    "musi",
    "mute",
    "namako",
    "nanpa",
    "nasa",
    "nasin",
    "nena",
    "ni",
    "nimi",
    "noka",
    "o",
    "oko",
    "olin",
    "ona",
    "open",
    "pakala",
    "pali",
    "palisa",
    "pan",
    "pana",
    "pi",
    "pilin",
    "pimeja",
    "pini",
    "pipi",
    "poka",
    "poki",
    "pona",
    "pu",
    "sama",
    "seli",
    "selo",
    "seme",
    "sewi",
    "sijelo",
    "sike",
    "sin",
    "sina",
    "sinpin",
    "sitelen",
    "sona",
    "soweli",
    "suli",
    "suno",
    "supa",
    "suwi",
    "tan",
    "taso",
    "tawa",
    "telo",
    "tenpo",
    "toki",
    "tomo",
    "tonsi",
    "tu",
    "unpa",
    "uta",
    "utala",
    "walo",
    "wan",
    "waso",
    "wawa",
    "weka",
    "wile",
]

REPLACEMENTS = {
    "a": "awa",
    "e": "en",
    "kalama": "kama",
    "uta": "usa",
    "li": "lin",
    "o": "ojo",
    "alasa": "asa",
    "pi": "pe",
    "la": "lan",
    "palisa": "pasa",
    "mu": "muju",
    "sinpin": "sipi",
    "kepeken": "peke",
    "sitelen": "site",
}

ONSETS = [''] + list('mnptkswlj')
VOWELS = list('aeiou')


def distinguish_coda_n(root: str):
    return (
        root
        .replace('n', 'N')
        .replace('Na', 'na')
        .replace('Ne', 'ne')
        .replace('Ni', 'ni')
        .replace('No', 'no')
        .replace('Nu', 'nu')
    )


def merge_rounded_vowels(root: str):
    return root.replace('u', 'o')


def make_replacements(root: str):
    return REPLACEMENTS.get(root, root)


def get_moras(root: str) -> list[str]:
    return list(re.findall(f"([{''.join(ONSETS)}]?[{''.join(VOWELS)}]|N)", distinguish_coda_n(root)))


def find_overlaps_helper(roots: list[str], shorter: list[str], longer: list[str], max_recursion: int):
    sstr = ''.join(shorter)
    lstr = ''.join(longer)
    assert lstr.startswith(sstr)

    for root in roots:
        if longer == [*shorter, root]:
            continue

        if (sstr + root).startswith(lstr):
            yield longer, [*shorter, root]

            if (sstr + root) != lstr and max_recursion > 0:
                yield from find_overlaps_helper(roots, longer, [*shorter, root], max_recursion - 1)


def find_overlaps(roots: list[str], max_recursion: int = 5):
    for root in roots:
        yield from find_overlaps_helper(roots, [], [root], max_recursion)


def find_used_moras(roots: list[str], first_only: bool = False):
    mora_counts: dict[str, int] = {}
    for root in roots:
        moras = get_moras(root)
        if first_only:
            moras = [moras[0]]
        for mora in moras:
            mora_counts[mora] = mora_counts.get(mora, 0) + 1

    print('   ', end='')
    for onset in ONSETS:
        print(f"{onset:<3}", end='')
    print()
    for vowel in VOWELS:
        print(vowel + '  ', end='')
        for onset in ONSETS:
            mora = onset + vowel
            if mora not in mora_counts:
                print('   ', end='')
            else:
                print(f"{mora_counts[mora]:<3}", end='')
        print()


def find_mora_distribution(roots: list[str]):
    roots_by_moras: dict[int, list[str]] = {
        n: []
        for n in range(1, 5)
    }

    for root in roots:
        moras = get_moras(root)
        roots_by_moras[len(moras)].append(root)

    for moras, roots in roots_by_moras.items():
        print(f"{len(roots)} roots with {moras} moras.")
        print(roots)


if __name__ == "__main__":
    # for a, b in find_overlaps(ROOTS):
    #     if ''.join(a) == ''.join(b):
    #         print(a, b)

    # roots = [make_replacements(root) for root in ROOTS]
    roots = ROOTS

    overlaps = list(find_overlaps(roots, 2))
    print(f"{len(overlaps)} overlaps.")
    for a, b in overlaps:
        print(a, b)
    print()

    # find_used_moras(ROOTS, first_only=True)
    find_mora_distribution(roots)
