import os

from scales import SCALES_31EDO


# Scale location functions


def scale_weight(scale, start=0):
    total = 0
    for j in range(len(scale)):
        total += j * scale[(start + j) % len(scale)]
    return total


def find_canon_rotation(scale):
    best_total = 10000
    best_rotation = None

    for i in range(len(scale)):
        total = scale_weight(scale, i)
        if total < best_total:
            best_total = total
            best_rotation = i

    return scale[best_rotation:] + scale[:best_rotation]


def find_all_scales(steps, possible_jumps, length):
    if steps <= 0 or length <= 0:
        return []

    for jump in possible_jumps:
        if steps == jump and length == 1:
            yield [jump]

        for scale in find_all_scales(steps - jump, possible_jumps, length - 1):
            yield [jump] + scale


def find_all_canonical_scales(steps, possible_jumps, length=12):
    try:
        os.makedirs(f"scales/{length}")
    except FileExistsError:
        pass

    filename = f"scales/{length}/{'_'.join([str(n) for n in possible_jumps])}.csv"
    scales = set()
    if os.path.exists(filename):
        with open(filename, "r") as fh:
            for line in fh.readlines():
                scales.add(tuple(int(n) for n in line.strip().split(",")))
    else:
        i = 0
        for scale in find_all_scales(steps, possible_jumps, length):
            if count18s(scale) / len(scale) > .5:
                canonical_scale = find_canon_rotation(scale)
                scales.add(tuple(canonical_scale))
            i += 1
            if i % 10000 == 0: print(i)
        with open(filename, "w") as fh:
            fh.writelines([str(scale)[1:-1] + "\n" for scale in sorted(list(scales))])

    return scales


# Scoring functions


def has_interval(l, start, interval):
    total = 0
    i = 0
    while total < interval:
        total += l[(start + i) % len(l)]
        # print(total, end=", ")
        i += 1
    # print(total == interval)
    return (total == interval)


def interval_diversity(scale, important_intervals=None):
    intervals = set()
    for rot in range(len(scale)):
        d = 0
        for deg in range(len(scale)):
            d += scale[(rot + deg) % len(scale)]
            intervals.add(d)

    if important_intervals:
        intervals = intervals & important_intervals

    return len(intervals)


def count_interval(scale, interval):
    total = 0
    for tonic in range(len(scale)):
        if has_interval(scale, tonic, interval):
            total += 1
    return total


def count18s(scale):
    return count_interval(scale, 18)


def count_chord_richness(l, intervals):
    totals = [0] * len(intervals)
    for start in range(len(l)):
        if has_interval(l, start, 18):
            for i, third in enumerate(intervals):
                if has_interval(l, start, third):
                    totals[i] += 1
    return min(*totals)


def count_total_chords(l, thirds):
    total = 0
    for start in range(len(l)):
        if has_interval(l, start, 18):
            for i, third in enumerate(thirds):
                if has_interval(l, start, third):
                    total += 1
    return total


def count_distinct_chord_roots(l, thirds):
    total = 0
    for start in range(len(l)):
        if has_interval(l, start, 18):
            has_third = False
            for i, third in enumerate(thirds):
                if has_interval(l, start, third):
                    has_third = True
            if has_third:
                total += 1
    return total


def count_extensions(scale, degrees):
    total = 0
    for start in range(len(scale)):
        if all(has_interval(scale, start, d) for d in degrees):
            total += 1
    return total


def count_present_consonances(scale, consonances):
    return len([c for c in consonances if count_interval(scale, c) > 0])


def count_dissonances(scale, consonances, edo_steps=31):
    return sum([count_interval(scale, d) for d in range(1, edo_steps) if d not in consonances])


def proper(scale):
    degrees = [set() for _ in range(len(scale) - 1)]
    for i, tonic in enumerate(scale):
        steps = 0
        for deg in range(1, len(scale)):
            steps += scale[(i + deg) % len(scale)]
            degrees[deg - 1].add(steps)

    not_strict = False
    for deg1, deg2 in zip(degrees[:-1], degrees[1:]):
        x, y = max(deg1), min(deg2)
        if x > y:
            return "improper"
        elif x == y:
            not_strict = True
    return "proper" if not_strict else "strictly proper"


def bool_scales(length, trues):
    if trues == 0:
        yield [False] * length
    elif trues == length:
        yield [True] * length
    else:
        for s in bool_scales(length - 1, trues):
            yield [False] + s
        for s in bool_scales(length - 1, trues - 1):
            yield [True] + s


def convert_subscale(bool_scale, scale):
    while not bool_scale[-1]:
        bool_scale = bool_scale[1:] + [bool_scale[0]]
        scale = scale[1:] + scale[:1]
    subscale = []
    steps = 0
    for jump, b in zip(scale, bool_scale):
        steps += jump
        if b:
            subscale.append(steps)
            steps = 0
    return tuple(find_canon_rotation(subscale))


def all_subscales(scale, length):
    subscale_set = set()
    for bool_scale in bool_scales(len(scale), length):
        subscale_set.add(convert_subscale(bool_scale, scale))
    return subscale_set


# Priority sequences


def fseries(*fs):
    return lambda scale: [f(scale) for f in fs]


h7n7_priorities = (
    lambda scale: interval_diversity(scale, {4, 7, 8, 9, 10, 25}),
    count18s,
    lambda scale: count_chord_richness(scale, [7, 8, 9, 10]),
    lambda scale: count_total_chords(scale, [8, 10])
)

diatonic_priorities = (count18s,)

dioudeteric_priorities = (
    lambda scale: count_chord_richness(scale, [7, 8, 9, 10, 11]),
    lambda scale: count_total_chords(scale, [7, 8, 9, 10, 11])
)

greek_letter_priorities = (
    lambda scale: interval_diversity(scale, {7, 25}),
    lambda scale: count_chord_richness(scale, [7, 8, 10]),
    lambda scale: count_total_chords(scale, [8, 10]),
    count18s
)

theta_subscale_priorities = (
    lambda scale: interval_diversity(scale, {6, 7, 25}),
    lambda scale: count_chord_richness(scale, [7, 8, 10]),
    lambda scale: count_total_chords(scale, [8, 10]),
    count18s
)

god_B_priorities = (
    lambda scale: interval_diversity(scale, {4, 7, 8, 9, 10, 25}),
    lambda scale: count_chord_richness(scale, [7, 8, 9, 10, 11]),
    lambda scale: count_total_chords(scale, [8, 10]),
    count18s
)

variety_priorities = (
    count18s,
    interval_diversity,
)


melodic_priorities = (
    lambda scale: tuple(SCALES_31EDO['no-step melodic nonatonic']) in all_subscales(scale, 9),
    lambda scale: (8, 5, 5, 3, 5, 5) in all_subscales(scale, 6),
    proper,
    interval_diversity,
)


harmonic_priorities = (
    lambda scale: (8, 5, 8, 5, 5) in all_subscales(scale, 5),
    lambda scale: interval_diversity(scale, {4, 6, 7, 9, 15}),
    lambda scale: count_distinct_chord_roots(scale, [7, 8, 10]),
    lambda scale: count_total_chords(scale, [7, 8, 10]),
    count18s,
)

consonances = {5, 6, 7, 8, 10, 11, 13, 15}
for c in consonances | set():
    consonances.add(31 - c)

consonance_priorities = (
    lambda scale: count_present_consonances(scale, consonances),
    lambda scale: -count_dissonances(scale, consonances | {3, 28}),
    lambda scale: count_total_chords(scale, [7, 8, 10])
)


# Final actions


def print_scale_heritage(scales, *check_parent_names):
    check_parent_subscales = [all_subscales(SCALES_31EDO[n], len(scales[0][0])) for n in check_parent_names]
    for scale, *scale_stats in scales:
        this_scale_names = []
        for scale_name, named_scale in SCALES_31EDO.items():
            if tuple(find_canon_rotation(named_scale)) == scale:
                this_scale_names.append(scale_name)

        parents = []
        for i in range(len(check_parent_names)):
            if scale in check_parent_subscales[i]:
                parents.append(f"({check_parent_names[i]})")

        print(scale, *scale_stats, *this_scale_names, *parents)


def find_scales(priorities_function, scale_size, intervals, *check_parent_names):
    scales = []
    methods = fseries(*priorities_function)
    for scale in find_all_canonical_scales(31, intervals, scale_size):
        if len(scale) == scale_size:
            scales.append((scale, *methods(scale)))
    scales.sort(key=lambda x: x[1:])
    print(len(scales))
    print_scale_heritage(scales[-1000:], *check_parent_names)


all_dodecatonics = [key for key, value in SCALES_31EDO.items() if len(value) == 12]

if __name__ == "__main__":
    find_scales(consonance_priorities, 8, [2, 3, 4, 5, 6, 7, 8, 9, 10])  # , *all_dodecatonics)
