import argparse
import math
import sys
from dataclasses import dataclass
from typing import Optional

from matplotlib import pyplot as plt

from utils import CategoryMap, Feature, FEATURES_FILE, load_features


CLPROB = "clprob"
ALL_PROBS = "all_probs"
MOST_SIMILAR = "most_similar"
COMPARE = "compare"
COMMANDS = (CLPROB, ALL_PROBS, MOST_SIMILAR, COMPARE,)


parser = argparse.ArgumentParser()
parser.add_argument("command", type=str, choices=COMMANDS, help="The type of analysis to perform")
parser.add_argument("lang", type=str, help="The language to analyze", nargs='?')
parser.add_argument("other_lang", type=str, help="The language to compare to", nargs='?')
parser.add_argument("-f", "--filename", type=str, default=FEATURES_FILE, help="The json feature data filename")
parser.add_argument("-n", "--natlang", action="store_true", help="If the language to analyze is a natlang")


# Features to skip because of data sparsity
SKIP_ANALYSIS = {
    "Writing Systems",
    "Position of Negative Morpheme With Respect to Subject, Object and Verb",
    "Order of Negative Morpheme and Verb",
}


FeatureSet = dict[str, Feature]
LangData = dict[str, str]


def _extract_cm_lang(lang: str, cm: CategoryMap) -> tuple[str, CategoryMap]:
    new_cm: CategoryMap = {}
    category = None

    for cat, langs in cm.items():
        if lang in langs:
            category = cat
            new_cm[cat] = langs - {lang}
        else:
            new_cm[cat] = langs

    return category, new_cm


def extract_lang(lang: str, features: FeatureSet, conlang: bool = True) -> tuple[LangData, FeatureSet]:
    lang_data: LangData = {}
    new_features: FeatureSet = {}

    for ID, feature in features.items():
        if conlang:
            category, conlangs = _extract_cm_lang(lang, feature.conlangs) if conlang else feature.conlangs
            natlangs = feature.natlangs
        elif feature.natlangs is None:
            conlangs = feature.conlangs
            natlangs = feature.natlangs
            category = None
        else:
            conlangs = feature.conlangs
            category, natlangs = _extract_cm_lang(lang, feature.natlangs)

        new_feature = Feature(
            name=feature.name,
            conlangs=conlangs,
            natlangs=natlangs,
        )

        new_features[ID] = new_feature
        if category is not None:
            lang_data[ID] = category

    return lang_data, new_features


def category_proportion(category: str, cm: CategoryMap) -> float:
    num, denom = None, 0

    for cat, langs in cm.items():
        denom += len(langs) + 1
        if cat == category:
            num = len(langs) + 1

    if num is None:
        print("Warning: num is None")
        num = 1

    return num/denom


def all_langs(features: FeatureSet, conlangs: bool) -> set[str]:
    out = set()

    for f in features.values():
        cm = f.conlangs if conlangs else f.natlangs

        if cm is None:
            continue

        for langs in cm.values():
            out = out | langs

    return out

@dataclass
class FeatureExplanation:
    ID: str
    feature_name: str
    category: str
    conlang_prob: float
    natlang_prob: float

    def to_scores(self) -> "AdjustedProbabilityScores":
        return AdjustedProbabilityScores(
            conlang_score=math.log2(self.conlang_prob),
            natlang_score=math.log2(self.natlang_prob),
        )


@dataclass
class AdjustedProbabilityScores:
    """Represents log probability scores *per feature*.

    This means it can be one of the two following things:
    - The log-scaled scores associated with a single feature
    - The sum of log-scaled scores for the features of a language, divided by how many features it is
      annotated for"""

    conlang_score: float
    natlang_score: float


@dataclass
class ConlangProbabilityAnalysis:
    conlang_score: float
    natlang_score: float
    explanations: list[FeatureExplanation]

    def conlang_score_per_feature(self):
        return self.conlang_score / len(self.explanations)

    def natlang_score_per_feature(self):
        return self.natlang_score / len(self.explanations)

    def adjust(self) -> "AdjustedProbabilityScores":
        return AdjustedProbabilityScores(
            conlang_score=self.conlang_score_per_feature(),
            natlang_score=self.natlang_score_per_feature(),
        )


def conlang_probability_analysis(lang_data: LangData, features: FeatureSet) -> ConlangProbabilityAnalysis:
    conlang_score, natlang_score = 0, 0

    feature_explanations: list[FeatureExplanation] = []

    for ID, cat in lang_data.items():
        if features[ID].natlangs is None:
            continue
        if features[ID].name in SKIP_ANALYSIS:
            continue

        cp = category_proportion(cat, features[ID].conlangs)

        try:
            np = category_proportion(cat, features[ID].natlangs)
        except TypeError:
            print(repr(features[ID].name), repr(cat), features[ID].natlangs.keys())
            raise

        exp = FeatureExplanation(ID, features[ID].name, cat, cp, np)

        if cp == 0 or np == 0:
            print(exp)

        feature_explanations.append(exp)

        conlang_score += math.log2(cp)
        natlang_score += math.log2(np)

    return ConlangProbabilityAnalysis(conlang_score, natlang_score, feature_explanations)


def contrastive_prob(score1: float, score2: float) -> float:
    diff = score1 - score2
    x = 2 ** diff
    return x / (1 + x)


@dataclass
class FeatureComparison:
    explanation: FeatureExplanation
    other_value: str

    def __post_init__(self):
        if self.explanation.category == self.other_value:
            self.similarity_score = -math.log2(self.explanation.natlang_prob)
        else:
            self.similarity_score = 0


@dataclass
class LanguageSimilarity:
    other_lang_name: str
    comparisons: list[FeatureComparison]

    def __post_init__(self):
        self.score: float = 0
        for comparison in self.comparisons:
            self.score += comparison.similarity_score

    def adjusted_score(self) -> Optional[float]:
        if len(self.comparisons) == 0:
            return None

        return self.score / len(self.comparisons)


def language_similarity(cpa: ConlangProbabilityAnalysis, features: FeatureSet, other_lang: str, conlang: bool)\
        -> LanguageSimilarity:
    other_lang_data, _ = extract_lang(other_lang, features, conlang)
    comparisons: list[FeatureComparison] = []

    for explanation in cpa.explanations:
        if explanation.ID in other_lang_data:
            comparisons.append(FeatureComparison(explanation, other_lang_data[explanation.ID]))

    return LanguageSimilarity(other_lang, comparisons)


def show_scores_histogram(scores: list[AdjustedProbabilityScores], title: str, bins: int = 50):
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=3)
    fig.suptitle(title)

    ax1.hist([s.natlang_score for s in scores], bins=bins, range=(-8, 0))
    ax1.set_title("Natlang scores")
    ax2.hist([s.conlang_score for s in scores], bins=bins, range=(-8, 0))
    ax2.set_title("Conlang scores")
    ax3.hist([s.conlang_score - s.natlang_score for s in scores], bins=bins, range=(-4, 4))
    ax3.set_title("Diff")

    plt.show()


def single_conlang_odds(lang_name, lang_data: LangData, features: FeatureSet):
    analysis = conlang_probability_analysis(lang_data, features)
    prob_is_conlang = contrastive_prob(analysis.conlang_score, analysis.natlang_score)

    feature_explanations: list[FeatureExplanation] = sorted(
        analysis.explanations,
        key=lambda e: math.log2(e.conlang_prob) - math.log2(e.natlang_prob),
    )

    print("Features from least to most conlangy:")

    crossed = False
    for exp in feature_explanations:
        scores = exp.to_scores()
        print(f"{exp.feature_name[:60]:<60} {exp.category:<45} cp: {exp.conlang_prob:.3f} np: {exp.natlang_prob:.3f}"
              f" net score: {scores.conlang_score - scores.natlang_score:.3f}")

        if not crossed and exp.conlang_prob > exp.natlang_prob:
            print("-"*120)
            crossed = True

    print()
    print(f"Probability that it is a conlang: {prob_is_conlang*100:.1f}%")
    print(f"Conlang score: {analysis.conlang_score:.3f}")
    print(f"Natlang score: {analysis.natlang_score:.3f}")
    print(f"Diff: {analysis.conlang_score - analysis.natlang_score:.3f}")
    print(f"Conlang score per feature: {analysis.conlang_score_per_feature():.3f}")
    print(f"Natlang score per feature: {analysis.natlang_score_per_feature():.3f}")

    show_scores_histogram(
        [e.to_scores() for e in feature_explanations],
        f"All features for {lang_name}"
    )


STAT_PAIRS = [
    ("conlang score", lambda s: s.conlang_score),
    ("natlang score", lambda s: s.natlang_score),
    ("diff", lambda s: s.conlang_score - s.natlang_score),
    ("adjusted conlang score", lambda s: s.conlang_score_per_feature()),
    ("adjusted natlang score", lambda s: s.natlang_score_per_feature()),
    ("adjusted diff", lambda s: s.conlang_score_per_feature() - s.natlang_score_per_feature()),
    ("num features", lambda s: len(s.explanations)),
]


def all_language_odds(features: FeatureSet, conlang: bool):
    langs = all_langs(features, conlangs=conlang)

    scores: list[tuple[str, ConlangProbabilityAnalysis]] = []

    for lang in langs:
        lang_data, extracted_features = extract_lang(lang, features, conlang=conlang)
        analysis = conlang_probability_analysis(lang_data, extracted_features)

        "Some languages may only be known from skipped features"
        if len(analysis.explanations) > 0:
            scores.append((lang, analysis))

    scores.sort(key=lambda x: x[1].conlang_score_per_feature() - x[1].natlang_score_per_feature())

    for i, (lang, score) in enumerate(scores):
        s = f"{i:<4} {lang:<25}"

        for name, f in STAT_PAIRS:
            s += f" | {name}: {f(score):.3f}"
        print(s)

    for name, f in STAT_PAIRS:
        stats = [f(s) for _, s in scores]
        print(f"Average {name}: {sum(stats)/len(stats):.3f}")

    show_scores_histogram(
        [s[1].adjust() for s in scores],
        "All conlangs" if conlang else "All natlangs",
    )


def most_similar_natlangs(lang_data: LangData, features: FeatureSet):
    natlangs = all_langs(features, conlangs=False)
    cpa = conlang_probability_analysis(lang_data, features)

    similarities = [
        language_similarity(cpa, features, lang, conlang=False)
        for lang in natlangs
    ]

    similarities = list(filter(lambda s: len(s.comparisons) >= 20, similarities))
    similarities.sort(key=lambda s: s.adjusted_score())

    print("Natlangs from most to least similar:")
    for i, s in enumerate(similarities):
        print(f"{i:<4} | {s.other_lang_name:<20} | score: {s.score} | num comparisons: {len(s.comparisons)}"
              f" | adjusted score: {s.adjusted_score()}")


def show_comparison(lang_data: LangData, features: FeatureSet, other_lang: str):
    cpa = conlang_probability_analysis(lang_data, features)
    similarity = language_similarity(cpa, features, other_lang, conlang=False)
    comparisons = sorted(similarity.comparisons, key=lambda c: c.similarity_score)

    for comp in comparisons:
        print(f"{comp.explanation.feature_name[:60]:<60} {comp.explanation.category:<30} {comp.other_value:<30}"
              f"{comp.similarity_score}")

    print()
    print("Overall similarity:", similarity.score)
    print("Num comparisons:", len(similarity.comparisons))
    print("Adjusted score:", similarity.adjusted_score())


if __name__ == "__main__":
    clargs = parser.parse_args()

    features = load_features(clargs.filename)

    lang_data = None
    if clargs.lang:
        lang_data, features = extract_lang(clargs.lang, features, conlang=not clargs.natlang)

    def require_lang():
        if lang_data is None:
            print("Please supply a language.")
            sys.exit(1)

    c = clargs.command

    if c == CLPROB:
        require_lang()
        single_conlang_odds(clargs.lang, lang_data, features)

    elif c == ALL_PROBS:
        all_language_odds(features, not clargs.natlang)

    elif c == MOST_SIMILAR:
        require_lang()
        most_similar_natlangs(lang_data, features)

    elif c == COMPARE:
        require_lang()
        show_comparison(lang_data, features, clargs.other_lang)



