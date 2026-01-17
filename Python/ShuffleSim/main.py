import random

import numpy as np


def get_deck(size: int = 60) -> list[int]:
    return [i for i in range(size)]


TRIALS = 1000
DECK_SIZE = 120
OVERHAND_SIZE = 15
OVERHAND_SIGMA = 4
CUT_SIGMA = 3

# Metrics


def get_inversion(deck: list[int]) -> int:
    invs = 0
    for i, card in enumerate(deck):
        invs += abs(i - card)
    if invs % 2 != 0:
        raise ValueError
    return invs//2


def get_neighbor_similarity(deck: list[int], neighborhood_size: int = 3):
    if len(deck) % neighborhood_size != 0:
        print(f"{len(deck)}")
    out = 0
    for i in range(0, len(deck), neighborhood_size):
        neighborhood = deck[i:i+neighborhood_size]

        for j in range(neighborhood_size):
            for k in range(j, neighborhood_size):
                out += abs(neighborhood[j] - neighborhood[k])
    return out


def colors_in_hand(deck: list[int], colors: int = 6, hand_size = 8):
    if len(deck) % colors != 0:
        raise ValueError
    color_size = len(deck)//colors

    if len(deck) % hand_size != 0:
        raise ValueError

    hand_colors = []
    for i in range(0, len(deck), hand_size):
        num_colors = len({
            card // color_size
            for card in deck[i:i+hand_size]
        })
        hand_colors.append(num_colors)

    return np.mean(hand_colors)


# Shuffles

def overhand_shuffle(deck: list[int], alternating: bool = False, mu: float = OVERHAND_SIZE, sigma: float = OVERHAND_SIGMA) -> list[int]:
    i = 0
    out = []
    front = True
    while i < len(deck):
        group_size = round(mu + sigma*np.random.normal())
        if group_size <= 0:
            continue
        next_i = min(len(deck), i + group_size)
        if front and alternating:
            out = out + deck[i:next_i]
        else:
            out = deck[i:next_i] + out
        i = next_i
        front = not front
    return out


def cut(deck: list[int], sigma: float = CUT_SIGMA) -> tuple[list[int], list[int]]:
    cut_point = round(len(deck)//2 + sigma*np.random.normal())
    return deck[:cut_point], deck[cut_point:]


def riffle_shuffle(deck: list[int], sigma: float = CUT_SIGMA) -> list[int]:
    left_half, right_half = cut(deck, sigma)

    left_i, right_i = 0, 0
    out = []
    while (left_i < len(left_half)) and (right_i < len(right_half)):
        if np.random.normal() < 0:
            out.append(left_half[left_i])
            left_i += 1
        else:
            out.append(right_half[right_i])
            right_i += 1

    out += left_half[left_i:]
    out += right_half[right_i:]

    return out


def cut_riffle(deck: list[int], reps: int, sigma: float = CUT_SIGMA) -> list[int]:
    left_half, right_half = cut(deck, sigma)
    for _ in range(reps):
        left_half = riffle_shuffle(left_half)
        right_half = riffle_shuffle(right_half)
    return  left_half + right_half


def pile_shuffle(deck: list[int], num_piles: int = 6):
    piles = []
    for _ in range(num_piles):
        piles.append([])
    for card in deck:
        piles[random.randrange(num_piles)].append(card)
    out = []
    for pile in piles:
        out += pile
    return out


def regular_pile_shuffle(deck: list[int], num_piles: int = 6):
    piles = []
    for _ in range(num_piles):
        piles.append([])
    for i, card in enumerate(deck):
        piles[i % num_piles].append(card)
    out = []
    for pile in piles:
        out += pile
    return out


def true_random_shuffle(deck: list[int]):
    np.random.shuffle(deck)
    return deck


def custom_shuffle(deck: list[int]) -> list[int]:
    alternating = False
    deck = overhand_shuffle(deck, alternating)
    deck = overhand_shuffle(deck, alternating)
    deck = overhand_shuffle(deck, alternating)
    deck = pile_shuffle(deck, 9)
    return deck


METHODS = [
    ('true random', true_random_shuffle),
    ('custom shuffle', custom_shuffle),
]

METRICS = [
    ('inv', get_inversion),
    ('neighbor', get_neighbor_similarity),
    ('colors', colors_in_hand),
]


if __name__ == "__main__":
    for method_name, method in METHODS:
        results = {
            metric_name: []
            for metric_name, _ in METRICS
        }

        for _ in range(TRIALS):
            deck = method(get_deck(DECK_SIZE))
            for metric_name, metric in METRICS:
                results[metric_name].append(metric(deck))

        print(method_name)
        for metric_name, _ in METRICS:
            print(f'  {metric_name:>10}: mu = {np.mean(results[metric_name]):>8.2f}, sigma = {np.std(results[metric_name]):>8.2f}')
        print()
