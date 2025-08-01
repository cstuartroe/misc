import random
import tqdm
import math


MAX = 150


def sequences(length: int):
    if length == 0:
        yield ()
    else:
        subseqs = sequences(length - 1)
        for seq in subseqs:
            yield (-1, *seq)
            yield (1, *seq)


def first_tie(seq) -> int | None:
    i = 0
    sum = 0

    for e in seq:
        sum += e
        i += 1
        if sum == 0:
            return i

    return None


def sequence_odds(flips: int) -> dict[int | None, int]:
    out = {}

    for seq in sequences(flips):
        tie_length = first_tie(seq)
        out[tie_length] = out.get(tie_length, 0) + 1

    return out


def flip_until_tie() -> int:
    flips = 1
    extra_heads = 1

    while extra_heads > 0 and flips < MAX:
        flips += 1
        extra_heads += 1 if random.random() > .5 else -1

    return flips


if __name__ == "__main__":
    n = 20
    flips = 2**n
    odds = sequence_odds(n)
    print(odds)
    for i in range(n+1):
        if i in odds:
            gcd = math.gcd(odds[i], flips)
            print(f"{odds[i]}/{flips} = {odds[i]//gcd}/{flips//gcd}")
    # flips_counts = {}
    # for _ in tqdm.tqdm(range(1000000000)):
    #     flips = flip_until_tie()
    #     flips_counts[flips] = flips_counts.get(flips, 0) + 1
    #
    # for flips in range(2, 102, 2):
    #     print(f"{flips:>3} {flips_counts.get(flips, 0):>10}")
