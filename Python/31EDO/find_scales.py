import os

from scales import SCALES_31EDO


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
            fh.writelines([str(scale)[1:-1]+"\n" for scale in sorted(list(scales))])

    return scales


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


def count_total_chords(l, intervals):
    total = 0
    for start in range(len(l)):
        if has_interval(l, start, 18):
            for i, third in enumerate(intervals):
                if has_interval(l, start, third):
                    total += 1
    return total


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


def all_subscales(scale, length):
    subscale_set = set()
    for bool_scale in bool_scales(len(scale), length):
        while not bool_scale[-1]:
            bool_scale = bool_scale[1:] + [bool_scale[0]]
        subscale = []
        steps = 0
        for jump, b in zip(scale, bool_scale):
            steps += jump
            if b:
                subscale.append(steps)
                steps = 0
        subscale_set.add(tuple(find_canon_rotation(subscale)))
    return subscale_set


def h7n7_priorities(scale):
    return (
        interval_diversity(scale, {4, 7, 8, 9, 10, 25}), count18s(scale), count_chord_richness(scale, [7, 8, 9, 10]),
        count_total_chords(scale, [8, 10]))


def diatonic_priorities(scale):
    return (count18s(scale),)


def dioudeteric_priorities(scale):
    return count_chord_richness(scale, [7, 8, 9, 10, 11]), count_total_chords(scale, [7, 8, 9, 10, 11])


def greek_letter_priorities(scale):
    return (
        interval_diversity(scale, {7, 25}), count_chord_richness(scale, [7, 8, 10]), count_total_chords(scale, [8, 10]),
        count18s(scale))


def theta_subscale_priorities(scale):
    return (
        interval_diversity(scale, {6, 7, 25}), count_chord_richness(scale, [7, 8, 10]),
        count_total_chords(scale, [8, 10]),
        count18s(scale))


def god_B_priorities(scale):
    return (interval_diversity(scale, {4, 7, 8, 9, 10, 25}), count_chord_richness(scale, [7, 8, 9, 10, 11]),
            count_total_chords(scale, [8, 10]), count18s(scale))


def variety_priorities(scale):
    return count18s(scale), interval_diversity(scale)


def find_scales(priorities_function, scale_size, intervals, *check_parent_names):
    check_parent_subscales = [all_subscales(SCALES_31EDO[n], scale_size) for n in check_parent_names]
    scales = []
    for scale in find_all_canonical_scales(31, intervals, scale_size):
        if len(scale) == scale_size:
            scales.append((scale, *priorities_function(scale)))
    scales.sort(key=lambda x: x[1:])
    print(len(scales))
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


if __name__ == "__main__":
    find_scales(variety_priorities, 7, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                "god chromatic B", "2,6 dioudeteric modified dodecatonic", "chromatic theta")
