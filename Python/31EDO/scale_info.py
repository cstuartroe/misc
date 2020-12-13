from scales import SCALE_REFS, DEGREE_REFS, DEGREES_31EDO
from find_scales import interval_diversity, count_interval, count18s, count_chord_richness, count_total_chords, proper


def print_scales(scale_name, edo):
    scale = SCALE_REFS[edo][scale_name]

    for i in range(len(scale)):
        steps = 0
        print("unison ", end="")
        for j in range(len(scale)):
            add = scale[(i + j) % len(scale)]
            steps += add
            print((f"+{add} " + str(DEGREE_REFS[edo][steps])).ljust(14, ' '), end="")
        assert (steps == edo)
        print()


def print_cents(scale_name, edo):
    scale = SCALE_REFS[edo][scale_name]
    steps = 0
    for jump in scale:
        steps += jump
        print(round(1200 * steps / edo))


# for subl in ([2, 3, 4, 4], [3, 2, 4, 4], [4, 4, 2, 3], [4, 4, 3, 2]):
#    l = [5] + subl + subl
#    print(l)
#    print_scales(l)


def scale_info(scale_name, extra_lines=None):
    print(scale_name)
    print_scales(scale_name, 31)
    print_cents(scale_name, 31)
    scale = SCALE_REFS[31][scale_name]
    print("Important interval diversity: %d/6" % interval_diversity(scale, {4, 7, 8, 9, 10, 25}))
    print("Total interval diversity: %d/31" % interval_diversity(scale))
    print(*[(DEGREES_31EDO[i], count_interval(scale, i)) for i in range(32)])
    print("Total chords:", *[count_total_chords(scale, [third]) for third in [7, 8, 9, 10, 11]])
    print("Proper:", proper(scale))
    for line in extra_lines or []:
        print(line)
    print()


if __name__ == "__main__":
    for scale in ("ultra melodic heptatonic",  "melodic octatonic 27 A",  "melodic octatonic 27 B",
                  "melodic dodecatonic 27",  "melodic octatonic 31 A",  "melodic octatonic 31 B",
                  "ultra melodic nonatonic", "melodic dodecatonic 31", "no-step melodic nonatonic"):
        scale_info(scale)
