import os
import sys
import string
from typing import Callable

OBVIOUSLY_INCLUDED = set(string.digits + string.ascii_letters)


def add_to_counts(counts: dict[str, int], file: str):
    with open(file, 'r') as fh:
        contents = fh.read()

    for c in contents:
        counts[c] = counts.get(c, 0) + 1


def character_counts(directory: str, match: Callable[[str], bool]):
    counts = {}

    for root, dirs, files in os.walk(directory, topdown=True):
        if "venv" in root:
            dirs[:] = []
            files[:] = []

        for file in files:
            if match(file):
                add_to_counts(counts, os.path.abspath(os.path.join(root, file)))

    return counts


if __name__ == "__main__":
    ext, directory = sys.argv[1:]

    counts = character_counts(directory, lambda filename: filename.endswith(ext))

    counts = sorted(list(counts.items()), key=lambda x: x[1], reverse=True)

    s = ''

    for c, count in counts:
        if c not in OBVIOUSLY_INCLUDED:
            s += c
            print(repr(c), count)

    print(repr(s))