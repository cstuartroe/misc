from typing import Optional
import numpy as np
import math
import wavio
from itertools import permutations
import random

random.seed(7)

RATE = 44100
SAMPWIDTH = 2

# Finish the audio file with a bit of silence
EXTRA_SECONDS = 1


def load_wav(filename: str) -> np.array:
    wav = wavio.read(filename)
    assert wav.rate == RATE
    assert wav.sampwidth == SAMPWIDTH
    return wav.data


KICK = load_wav("kick.wav")
SNAR = load_wav("snare.wav")
STIK = load_wav("stick.wav")


Measure = list[Optional[np.array]]


def generate_wav(
        measures: list[Measure],
        beats_per_minute: int,
        eighths_per_measure: int = 9,
) -> np.array:
    print(len(measures), "measures")
    eighth_note_seconds = 30/beats_per_minute
    measure_seconds = eighths_per_measure*eighth_note_seconds
    total_seconds = len(measures)*measure_seconds + EXTRA_SECONDS
    print(total_seconds, "seconds")
    total_seconds = math.ceil(total_seconds)

    wav = np.zeros((total_seconds*RATE, SAMPWIDTH), dtype=int)

    for i, measure in enumerate(measures):
        assert len(measure) == eighths_per_measure
        measure_begin_seconds = i*measure_seconds

        for j, sound in enumerate(measure):
            if sound is None:
                continue

            sound_begin_seconds = measure_begin_seconds + j*eighth_note_seconds

            sound_begin_frames = int(sound_begin_seconds*RATE)

            sound_frames, sampwidth = sound.shape
            assert sampwidth == SAMPWIDTH

            wav[sound_begin_frames:sound_begin_frames + sound_frames, :] = sound

    return wav


def all_triples(l: list) -> list:
    out = []
    for e in l:
        out += [e]*3
    return out


def drop_beat_permutations(
        measure: Measure,
        beats: list[int],
) -> list[list[Measure]]:
    """Every permutation of gradually dropping out beats."""
    out = []

    for perm in permutations(beats):
        current = [*measure]
        group = [[*current]]
        for i in perm:
            current[i] = None
            group.append([*current])
        out.append(group)

    return out


def mirror(l: list):
    return l + l[::-1][1:]


SNARES_333: Measure = [KICK, STIK, STIK, SNAR, STIK, STIK, SNAR, STIK, STIK]
SKIPS_333 = [1, 2, 4, 5, 7, 8]

SNARES_2223 = [KICK, STIK, SNAR, STIK, SNAR, STIK, SNAR, STIK, STIK]
SKIPS_2223 = [1, 3, 5, 7, 8]

SNARES_2232 = [KICK, STIK, SNAR, STIK, SNAR, STIK, STIK, SNAR, STIK]
SKIPS_2232 = [1, 3, 5, 6, 8]
SKIPS_2232_333 = [1, 5, 8]


ALL_STICKS: Measure = [KICK] + 8*[STIK]


def generate_note_dropping_examples(bpm: int):
    measures = []

    dropping_out_examples = round(bpm/10) - 1
    print(bpm, "BPM:", dropping_out_examples, "examples")

    # First, establish triplets
    dropping_to_333 = drop_beat_permutations(SNARES_333, SKIPS_333)
    random.shuffle(dropping_to_333)
    for group in dropping_to_333[:dropping_out_examples]:
        measures += group

    # Establish a 2223 feel by dropping out eighths
    dropping_to_2223 = drop_beat_permutations(SNARES_2223, SKIPS_2223)
    random.shuffle(dropping_to_2223)
    for group in dropping_to_2223[:dropping_out_examples]:
        measures += group

    # Do the same with 2232 feel
    dropping_to_2232 = drop_beat_permutations(SNARES_2232, SKIPS_2232)
    random.shuffle(dropping_to_2232)
    for group in dropping_to_2232[:dropping_out_examples]:
        measures += group

    # Do the mixed triplet-2232 feel two different ways
    # Only 3 beats dropping => 6 combos, so no need to sample
    dropping_to_mixed = drop_beat_permutations(SNARES_333, SKIPS_2232_333)
    random.shuffle(dropping_to_mixed)
    for group in dropping_to_mixed:
        measures += group

    dropping_to_mixed = drop_beat_permutations(SNARES_2232, SKIPS_2232_333)
    random.shuffle(dropping_to_mixed)
    for group in dropping_to_mixed:
        measures += group

    # Throw in some random arrangements
    dropping_randomly = drop_beat_permutations(ALL_STICKS, [1, 2, 3, 4, 5, 6, 7, 8])
    random.shuffle(dropping_randomly)
    for group in dropping_randomly[:dropping_out_examples]:
        measures += group[:-3]

    wav = generate_wav(
        all_triples(measures),
        bpm,
    )

    wavio.write(f"{bpm}bpm.wav", wav, rate=RATE, sampwidth=SAMPWIDTH)


if __name__ == "__main__":
    for bpm in [70, 80, 90, 105, 120, 140]:
        generate_note_dropping_examples(bpm)


