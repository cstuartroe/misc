from dataclasses import dataclass
from enum import Enum
import random
from random import randrange


random.seed(104)


class InvalidPhoneme(ValueError):
    pass


def pick_weighted[T](choices: dict[T, int]) -> T:
    total = sum(choices.values())
    n = randrange(total)

    cumulative_sum = 0
    for choice, weight in choices.items():
        cumulative_sum += weight
        if n < cumulative_sum:
            return choice


class VowelQuality(Enum):
    # plain, nasal, post-uvular
    A = ("a", "o", "a")
    I = ("i", "i", "e")
    U = ("u", "o", "o")


quality_weights: dict[VowelQuality, int] = {
    VowelQuality.A: 5,
    VowelQuality.I: 3,
    VowelQuality.U: 2,
}


class VowelPhonation(Enum):
    HIGH = "high"
    LOW = "low"
    CHECKED = "checked"
    NASAL = "nasal"


phonation_weights: dict[VowelPhonation, int] = {
    VowelPhonation.HIGH: 1,
    VowelPhonation.LOW: 2,
    VowelPhonation.CHECKED: 1,
    VowelPhonation.NASAL: 1,
}


@dataclass
class Vowel:
    quality: VowelQuality
    phonation: VowelPhonation

    @classmethod
    def random(cls):
        while True:
            q = pick_weighted(quality_weights)
            p = pick_weighted(phonation_weights)
            try:
                return cls(q, p)
            except InvalidPhoneme:
                pass


class POA(Enum):
    LABIAL = "labial"
    ALVEOLAR_APICAL = "alveolar apical"
    ALVEOLAR_LATERAL = "alveolar lateral"
    # not an actual place of articulation, but functions as though it is in this phonology
    SIBILANT = "sibilant"
    VELAR = "velar"
    UVULAR = "uvular"


class MOA(Enum):
    NASAL = "nasal"
    OBSTRUENT = "obstruent"
    APPROXIMANT = "approximant"


@dataclass
class Consonant:
    poa: POA
    moa: MOA

    initial_romanization: str
    intervocal_romanization: str | None
    nasal_romanization: str | None
    checked_romanization: str | None


class ExtantConsonant(Enum):
    M = Consonant(POA.LABIAL, MOA.NASAL, "m", None, None, None)
    N = Consonant(POA.ALVEOLAR_APICAL, MOA.NASAL, "n", None, None, None)  # actually is [l] but structurally acts nasal

    P = Consonant(POA.LABIAL, MOA.OBSTRUENT, "p", "v", "m", "pp")
    T = Consonant(POA.ALVEOLAR_APICAL, MOA.OBSTRUENT, "t", "r", "nr", "tt")
    L = Consonant(POA.ALVEOLAR_LATERAL, MOA.OBSTRUENT, "l", "l", "n", "tl")  # [ɬ] word-initially
    C = Consonant(POA.SIBILANT, MOA.OBSTRUENT, "c", "j", "nj", "cc")
    K = Consonant(POA.VELAR, MOA.OBSTRUENT, "k", "g", "ng", "kk")
    Q = Consonant(POA.UVULAR, MOA.OBSTRUENT, "q", "h", "nq", "qq")

    V = Consonant(POA.LABIAL, MOA.APPROXIMANT, "v", None, None, None)
    J = Consonant(POA.SIBILANT, MOA.APPROXIMANT, "j", None, None, None)
    GLOTTAL_STOP = Consonant(POA.VELAR, MOA.APPROXIMANT, "", None, None, None)


initial_consonant_weights: dict[ExtantConsonant, int] = {
    ExtantConsonant.M: 51,
    ExtantConsonant.N: 64,
    ExtantConsonant.P: 13,
    ExtantConsonant.T: 100,
    ExtantConsonant.L: 21,
    ExtantConsonant.C: 17,
    ExtantConsonant.K: 80,
    ExtantConsonant.Q: 26,
    ExtantConsonant.V: 33,
    ExtantConsonant.J: 41,
    ExtantConsonant.GLOTTAL_STOP: 200,
}

medial_consonant_weights: dict[ExtantConsonant, int] = {
    ExtantConsonant.P: 33,
    ExtantConsonant.T: 100,
    ExtantConsonant.L: 51,
    ExtantConsonant.C: 41,
    ExtantConsonant.K: 80,
    ExtantConsonant.Q: 64,
}


@dataclass
class Syllable:
    consonant: ExtantConsonant
    vowel: Vowel

    def vowel_romanization(self):
        plain, nasal, uvular = self.vowel.quality.value
        if self.consonant.value.poa is POA.UVULAR:
            return uvular
        elif self.vowel.phonation is VowelPhonation.NASAL:
            return nasal
        else:
            return plain


@dataclass
class Word:
    syllables: list[Syllable]

    def __post_init__(self):
        for i in range(len(self.syllables) - 1):
            if (
                    (self.syllables[i].vowel.phonation in (VowelPhonation.HIGH, VowelPhonation.CHECKED))
                    and (self.syllables[i + 1].vowel.phonation is VowelPhonation.HIGH)
            ):
                self.syllables[i + 1].vowel.phonation = VowelPhonation.LOW

            if self.syllables[i + 1].consonant.value.moa is not MOA.OBSTRUENT:
                raise ValueError

    def romanization(self):
        out = ""
        out += self.syllables[0].consonant.value.initial_romanization
        out += self.syllables[0].vowel_romanization()

        for i in range(len(self.syllables) - 1):
            c = self.syllables[i + 1].consonant.value

            intervocal_romanization = c.intervocal_romanization
            if (
                    (self.syllables[i + 1].consonant is ExtantConsonant.K)
                    and (self.syllables[i + 1].vowel.quality is VowelQuality.U)
                    and (self.syllables[i + 1].vowel.phonation is not VowelPhonation.NASAL)
            ):
                intervocal_romanization = "v"

            match self.syllables[i].vowel.phonation:
                case VowelPhonation.LOW:
                    out += intervocal_romanization
                case VowelPhonation.HIGH:
                    out += "h" + intervocal_romanization
                case VowelPhonation.NASAL:
                    out += c.nasal_romanization
                case VowelPhonation.CHECKED:
                    out += c.checked_romanization

            out += self.syllables[i + 1].vowel_romanization()

        match self.syllables[-1].vowel.phonation:
            case VowelPhonation.LOW:
                pass
            case VowelPhonation.HIGH:
                out += "h"
            case VowelPhonation.NASAL:
                out += "n"
            case VowelPhonation.CHECKED:
                out += "t"

        return out


def make_random_word(num_syllables: int) -> Word:
    syllables = []

    for i in range(num_syllables):
        if i == 0:
            c = pick_weighted(initial_consonant_weights)
        else:
            c = pick_weighted(medial_consonant_weights)
        v = Vowel.random()

        syllables.append(Syllable(c, v))

    return Word(syllables)


def generate_some_words():
    syllable_number: dict[int, int] = {
        1: 3,
        2: 6,
        3: 2,
        4: 1,
    }

    for _ in range(20):
        word = make_random_word(pick_weighted(syllable_number))
        print(word.romanization(), end=" ")

    print()


def estimate_possible_words():
    for i in range(25):
        words = set()
        for _ in range(2**i):
            word = make_random_word(2)
            words.add(word.romanization())

        print(len(words))


# def generate_sentences():
words: dict[str, int] = {}
for i in range(10000):
    frequency = round(100000/(i+1))
    syllable_number = {
        1: 200,
        2: 100 + 2*i,
        3: 3*i,
        4: 1*i,
    }
    word = make_random_word(pick_weighted(syllable_number))
    words[word.romanization()] = frequency
    # print(word.romanization(), frequency)

text = ""
for _ in range(30):
    sentence = " ".join([pick_weighted(words) for _ in range(randrange(2, 20))]).capitalize() + ". "
    text += sentence
print(text)
print()

letter_frequencies = {}
for letter in text:
    if letter in ". ":
        continue
    letter_frequencies[letter.lower()] = letter_frequencies.get(letter.lower(), 0) + 1

total = sum(letter_frequencies.values())
for letter, count in sorted(list(letter_frequencies.items()), key=lambda x: -x[1]):
    print(f"{letter} {count*100/total:.2f}%")
