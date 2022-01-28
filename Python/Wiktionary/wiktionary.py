import requests
from tqdm import tqdm
import os
import json


CONSONANTS = "mnptckbdjgwlrysh"
VOWELS = "aeiou"

CACHE_FILENAME = "num_definitions.txt"


def definitions(word):
    req = requests.get(
        url=f"https://en.wiktionary.org/api/rest_v1/page/definition/{word}"
    )

    return req.json()


def num_definitions(word):
    req = requests.get(
        url=f"https://en.wiktionary.org/wiki/{word}"
    )

    return req.text.count('toclevel-1')


def get_all_num_definitions():
    nm = {}

    if os.path.exists(CACHE_FILENAME):
        with open(CACHE_FILENAME, 'r') as fh:
            for line in fh.readlines():
                word, count = line.strip().split(' ')
                nm[word] = int(count)

    words = []
    for c1 in CONSONANTS:
        for v1 in VOWELS:
            for c2 in CONSONANTS:
                for v2 in VOWELS:
                    word = c1 + v1 + c2 + v2
                    words.append(word)

    for word in tqdm(words):
        if word not in nm:
            nm[word] = num_definitions(word)

    return nm


def find_max_words():
    nm = sorted(list(get_all_num_definitions().items()), key=lambda x: x[1])

    with open(CACHE_FILENAME, 'w') as fh:
        for word, count in nm:
            fh.write(f"{word} {count}\n")

    for word, count in nm:
        if count > 0:
            print(word, count)

    print(f"In all, {len(list(filter(lambda x: x[1] > 0, nm)))}/{len(nm)} words had definitions in at least one language")


def find_max_phonemes():
    consonant_frequencies = {}
    vowel_frequencies = {}

    for word, count in get_all_num_definitions().items():
        consonant_frequencies[word[0]] = consonant_frequencies.get(word[0], 0) + count
        consonant_frequencies[word[2]] = consonant_frequencies.get(word[2], 0) + count

        vowel_frequencies[word[1]] = vowel_frequencies.get(word[1], 0) + count
        vowel_frequencies[word[3]] = vowel_frequencies.get(word[3], 0) + count

    print("Consonant counts")

    for c, count in sorted(list(consonant_frequencies.items()), key=lambda x: x[1]):
        print(c, count)

    print()

    print("Vowel counts")

    for v, count in sorted(list(vowel_frequencies.items()), key=lambda x: x[1]):
        print(v, count)


find_max_words()

find_max_phonemes()
