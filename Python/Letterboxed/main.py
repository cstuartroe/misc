import sys


UNIX_WORDS = "/usr/share/dict/words"
WIKTIONARY_WORDS = "../wiki-100k.txt"


def construct_continuation_graph() -> dict[str, set[str]]:
    letter_groups = sys.argv[1:]

    assert len(letter_groups) == 4
    assert all(len(group) == 3 for group in letter_groups)

    graph = {}
    for g1 in letter_groups:
        for l1 in g1:
            l1 = l1.upper()

            assert l1 not in graph
            graph[l1] = set()

            for g2 in letter_groups:
                if g1 == g2:
                    continue

                for l2 in g2:
                    l2 = l2.upper()

                    graph[l1].add(l2)

    return graph


def load_words_from(wordlist_file) -> list[str]:
    with open(wordlist_file, "r") as fh:
        words = [
            line.strip()
            for line in fh.readlines()
        ]

    print(f"{wordlist_file} has {len(words)} words")
    words = sorted(list(set([
        word.upper()
        for word in words
        if not word.startswith("#")
    ])))
    print(f"{wordlist_file} has {len(words)} cleaned words")
    return words


def load_words():
    unix_words = load_words_from(UNIX_WORDS)
    wikt_words = load_words_from(WIKTIONARY_WORDS)

    print(f"{(len(set(unix_words) | set(wikt_words)))} cleaned words appear in either list")
    print(f"{(len(set(unix_words) & set(wikt_words)))} cleaned words appear in both lists")

    return sorted(list(set(unix_words) & set(wikt_words)))


def match_boxes(word: str, graph: dict[str, set[str]]):
    for i in range(len(word) - 1):
        l1, l2 = word[i], word[i+1]
        if l2 not in graph.get(l1, []):
            return False
    return True


def generate_chains(words: list[str], by_first_letter: dict[str, list[str]], length: int):
    if length == 0:
        yield ()

    else:
        for word in words:
            for chain in generate_chains(by_first_letter[word[-1]], by_first_letter, length - 1):
                yield word, *chain


def main():
    g = construct_continuation_graph()
    words = load_words()
    print(words[:10])
    print(f"{len(words)} words in the dictionary.")

    matching_words = set()
    for word in load_words():
        word = word.upper()
        if match_boxes(word, g):
            matching_words.add(word)
    print(f"{len(matching_words)} words possible to play with this set of boxes")
    matching_words = sorted(list(matching_words))

    words_by_first_letter = {}
    for word in matching_words:
        if word[0] not in words_by_first_letter:
            words_by_first_letter[word[0]] = []
        words_by_first_letter[word[0]].append(word)

    chains = []
    for chain in generate_chains(matching_words, words_by_first_letter, 3):
        if len(set(''.join(chain))) == 12:
            chains.append(chain)
    for chain in chains:
        print(chain)


if __name__ == "__main__":
    main()
