import math
import random


# E.g., 49°05'21.66"N 91°02'41.09"E

def generate_point() -> tuple[float, float]:
    latitude = (math.acos(random.random()*2 - 1))/math.pi - .5
    longitude = random.random()*2 - 1

    return latitude, longitude


def split(x: float):
    return math.floor(x), x % 1


def pi_radians_to_coords(r: float, neg_dir: str, pos_dir: str) -> str:
    degrees, rest = split(abs(r)*180)
    minutes, rest = split(rest*60)
    seconds = round(rest*60, 2)
    return f"{degrees}°{minutes:>02}'{seconds:>05}\"" + (neg_dir if r < 0 else pos_dir)


def point_to_coords(point: tuple[float, float]) -> str:
    return f"{pi_radians_to_coords(point[0], 'N', 'S')} {pi_radians_to_coords(point[1], 'W', 'E')}"


if __name__ == "__main__":
    print(point_to_coords(generate_point()))
