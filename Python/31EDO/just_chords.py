import math
from tabulate import tabulate
from consonance import vogel_dissonance, euler_dissonance, cents, gill_purves_dissonance

NAMED_CHORDS = {
    (1, 2): "octave",
    (2, 3): "perfect fifth",
    (3, 4): "perfect fourth",
    (3, 5): "major sixth",
    (4, 5): "major third",
    (5, 6): "minor third",
    (5, 8): "minor sixth",
    (8, 9): "large major second",
    (4, 7): "septimal minor seventh",
    (5, 9): "large minor seventh",
    (9, 16): "small minor seventh",
    (6, 7): "septimal minor third",
    (7, 8): "septimal major second",
    (8, 15): "major seventh",
    (9, 10): "small major second",
    (5, 7): "small septimal tritone",
    (7, 9): "septimal major third",
    (7, 12): "septimal major sixth",
    (15, 16): "large semitone",
    (16, 27): "pythagorean major sixth",
    (7, 10): "large septimal tritone",
    (9, 14): "septimal minor sixth",
    (27, 32): "pythagorean minor third",

    (6, 8, 9): "sus4",
    (8, 9, 12): "sus2",
    (3, 4, 5): "major",
    (9, 12, 16): "suspended (quartal)",
    (10, 12, 15): "minor",
    (5, 6, 9): "m7 w/out 5",
    (8, 10, 15): "maj7 w/out 5",
    (8, 12, 15): "maj7 w/out 3",
    (4, 6, 7): "septimal m7 w/out 3",
    (5, 8, 9): "E C D",
    (8, 9, 15): "C D B",
    (9, 10, 15): "m7 w/out 3",
    (4, 5, 7): "septimal dom7 w/out 5",
    (6, 7, 9): "septimal minor",
    (7, 8, 9): "septimal Bb C D",
    (5, 6, 7): "septimal diminished",

    (8, 10, 12, 15): "maj7",
    (10, 12, 15, 16): "m6",
    (10, 12, 15, 18): "m7",
    (16, 18, 24, 27): "sus2 add6",
}


ORDINALS = [
    "0th",
    "1st",
    "2nd",
    "3rd",
]


def get_chord_name(chord):
    if chord in NAMED_CHORDS:
        return NAMED_CHORDS[chord]

    uninverted = chord
    inv = 0
    while uninverted[-1] % 2 == 0:
        inv += 1
        uninverted = (uninverted[-1]//2, *uninverted[:-1])
        if uninverted in NAMED_CHORDS:
            return f"{NAMED_CHORDS[uninverted]} ({ORDINALS[inv]} inversion)"

    uninverted = chord
    for uninv in range(1, len(chord)):
        uninverted = (*uninverted[1:], uninverted[0] * 2)
        if uninverted in NAMED_CHORDS:
            return f"{NAMED_CHORDS[uninverted]} ({ORDINALS[len(chord) - uninv]} inversion)"

    return "unnamed"


CHORD_MAX = 100


def chords_helper(tones, start=2):
    if tones == 0:
        return [()]
    else:
        out = []
        for tonic in range(start, CHORD_MAX + 1):
            for tail in chords_helper(tones - 1, tonic + 1):
                out.append((tonic, *tail))
        return out


def chords(tones=3):
    return [chord for chord in chords_helper(tones) if math.gcd(*chord) == 1 and (chord[-1] / chord[0] < 2)]


def chords_with_dissonance(tones=3, dissonance_function=euler_dissonance):
    out = []

    for chord in chords(tones):
        out.append((chord, dissonance_function(*chord)))

    out.sort(key=lambda x: x[1])
    return out


def closest_approximation(r, edo_steps):
    r_cents = cents(r)
    step_size = 1200 / edo_steps
    steps = round(r_cents / step_size)
    return round((steps * step_size) - r_cents, 1)


MAJOR_EDOS = [12, 17, 19, 22, 24, 31, 41]


if __name__ == "__main__":
    table = [
        (
            "Ratio",
            "Dissonance",
            "Name",
            "Cents",
            *(
                f"{s}EDO Approximation"
                for s in MAJOR_EDOS
            )
        )
    ]

    for chord, dissonance in chords_with_dissonance(2, dissonance_function=euler_dissonance):
        table.append((
            ':'.join(map(str, chord)),
            dissonance,
            NAMED_CHORDS.get(chord, ''),
            cents(chord[1]/chord[0]),
            *(
                closest_approximation(chord[1]/chord[0], edo_steps)
                for edo_steps in MAJOR_EDOS
            ),
        ))

    print(tabulate(table))
