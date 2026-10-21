import re

WORD_RE = "[DTa-zéàèäëïöüêîûçñ3'-]+"

def pull_percents():
    with open("extracted_text.txt", "r") as fh:
        lines = fh.read().split("\n")

    words = []

    for line in lines:
        if line == "spelling % Bel % Ned":
            pass
        elif re.fullmatch("woordenkennis.book Page [0-9]+ Tuesday, June 10, 2014 4:45 PM", line):
            pass
        elif re.fullmatch("[A-Z]", line):
            pass
        elif re.fullmatch("[0-9]+", line):
            pass
        elif re.fullmatch(f"{WORD_RE} [0-9]+ [0-9]+", line):
            word, bel, ned = line.split(" ")
            words.append((word, int(bel), int(ned)))
        elif re.fullmatch(f"{WORD_RE} {WORD_RE}", line):
            pass
        else:
            raise ValueError

    return words


if __name__ == "__main__":
    words = pull_percents()

    num_words_by_knowledge = {
        n: 0
        for n in range(101)
    }

    for word in words:
        num_words_by_knowledge[word[2]] += 1

    cumul_words = 0
    for i in range(100, -1, -1):
        cumul_words += num_words_by_knowledge[i]

        print(f"{i}% of Nederlanders know {cumul_words} words")

    for n in [100, 99, 98, 97, 95, 90, 80, 50]:
        selected_words = [w for w in words if w[2] >= n]
        with open(f"wordlists/{n}.txt", "w") as fh:
            for word, _, _ in selected_words:
                fh.write(word + "\n")
