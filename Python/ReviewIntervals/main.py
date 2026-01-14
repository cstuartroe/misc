from dataclasses import dataclass
import random
from matplotlib import pyplot as plt


@dataclass
class Difficulty:
    factor: float
    max_days: int


FUZZ = .1


difficulties = {
    "wrong": Difficulty(0, 1),
    "difficult": Difficulty(.35, 14),
    "fine": Difficulty(1.3, 90),
    "easy": Difficulty(2.6, 365),
}


def next_interval(last_interval: int, difficulty: Difficulty) -> int:
    average_interval = min(last_interval*difficulty.factor + 1, difficulty.max_days)
    fuzz_factor = 1 + 2*FUZZ*random.random() - FUZZ
    return round(average_interval * fuzz_factor)


TRIALS = 15


def graph_days(start: int, difficulty: Difficulty):
    for i in range(TRIALS):
        print(f"{i+1:>3}) ", end="")
    print()

    for trial in range(10):
        days = [start]
        for _ in range(TRIALS):
            ni = next_interval(days[-1], difficulty)
            print(f"{ni:>3}, ", end="")
            days.append(ni)

        print()
        plt.plot(days)

    plt.show()


if __name__ == "__main__":
    for difficulty, start in [
        ("wrong", 100),
        ("difficult", 100),
        ("difficult", 0),
        ("fine", 0),
        ("easy", 0),
    ]:
        print("------------------------------")
        print(f"{difficulty:<10} {start:>3}")
        graph_days(start, difficulties[difficulty])
