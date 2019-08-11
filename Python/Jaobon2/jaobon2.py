import os
import json
import sys

FILENAME = "jaobon2.json"

ONSETS = ['m', 'n', 'p', 't', 'c', 'k', 'b', 'd', 'j', 'g', 's', 'x', 'h', 'w', 'l', 'y']

FINALS = ['a', 'ai', 'ak', 'an', 'ao', 'as',
          'e', 'ek', 'en', 'es',
          'i', 'ik', 'in', 'is',
          'o', 'ok', 'on', 'os',
          'u', 'uk', 'un', 'us']

FORBIDDEN_SEQUENCES = ['ti', 'di', 'si', 'yi', 'hi', 'wu']


EMPTY_ROOT = {
    "definition": None,
    "sources": [{
        "language": None,
        "word": None
    }],
    "hanzi": None
}

LEVEL_NAMES = ["nature", "pta", "food", "profs", "society"]


def possible_syllables():
    syllables = set()

    for f in FINALS:
        syllables.add(f)
        for o in ONSETS:
            syll = o + f
            if all(s not in syll for s in FORBIDDEN_SEQUENCES):
                syllables.add(syll)

    return syllables


def join_syllables(sylls):
    out = sylls[0]
    for syll in sylls[1:]:
        if syll[0] in "aeiou":
            out += "'"
        out += syll
    return out


if os.path.exists(FILENAME):
    with open(FILENAME, "r") as fh:
        jaobon_json = json.load(fh)
else:
    jaobon_json = {"roots": {}, "invalid_roots": {}, "undefined_roots": {}}


if "makesylls" in sys.argv:
    possible_roots = jaobon_json["undefined_roots"]
    possible_roots.update(jaobon_json["roots"])

    syllables = possible_syllables()
    print(len(syllables), "syllables possible.")
    for syll in syllables:
        if syll not in possible_roots:
            if syll in jaobon_json["invalid_roots"]:
                possible_roots[syll] = jaobon_json["invalid_roots"][syll]
                del jaobon_json["invalid_roots"][syll]
            else:
                possible_roots[syll] = EMPTY_ROOT

    jaobon_json["roots"] = {}
    jaobon_json["undefined_roots"] = {}

    for syll, root in possible_roots.items():
        if syll not in syllables:
            jaobon_json["invalid_roots"][syll] = possible_roots[syll]
            del possible_roots[syll]
        elif root is None or root["definition"] is None:
            jaobon_json["undefined_roots"][syll] = root or EMPTY_ROOT
        else:
            jaobon_json["roots"][syll] = root

    print(f"{len(jaobon_json['roots'])} roots defined.")

elif "sources" in sys.argv:
    sources = {}
    num_sources = 0

    for syll, root in jaobon_json["roots"].items():
        for source in root["sources"]:
            lang = source["language"] or "null"
            x = 1/len(root["sources"]) if '-c' in sys.argv else 1
            num_sources += x
            sources[lang] = sources.get(lang, 0) + x
            if lang == "zh" and root["hanzi"] is None and len(source["word"]) == 1:
                root["hanzi"] = source["word"]

    print(f"{round(num_sources)} sources listed for {len(jaobon_json['roots'])} defined roots.")
    for lang, count in sorted(list(sources.items()), key=lambda x: x[0]):
        print(f"{str(round(count, 2)).ljust(5, ' ')} "
              f"({str(round(100*count/(num_sources if '-c' in sys.argv else len(jaobon_json['roots'])))).rjust(2,' ')}%) "
              f"{lang} sources listed.")

elif "validate" in sys.argv:
    for c in jaobon_json["compounds"]:
        try:
            assert(type(c["definition"]) == str)
            assert(all(s in jaobon_json["roots"] for s in c["syllables"]))
            assert(len(c["tags"]) > 0)
            assert(all(t in LEVEL_NAMES for t in c["tags"]))
        except BaseException as e:
            print(f"{type(e).__name__}: {e}")
            print(json.dumps(c, indent=2))

elif "csv" in sys.argv:
    sorted_sylls = sorted(list(jaobon_json["roots"].keys()))
    with open("sylls.csv", "w") as fh:
        for syll in sorted_sylls:
            fh.write(f"{syll}\t{jaobon_json['roots'][syll]['definition']}\n")

    for level_name in LEVEL_NAMES:
        compounds = [c for c in jaobon_json["compounds"]
                     if level_name in c["tags"]]
        compounds.sort(key=lambda c: join_syllables(c['syllables']))

        with open(f"{level_name}.csv", "w") as fh:
            for c in compounds:
                fh.write(f"{join_syllables(c['syllables'])}\t{c['definition']}\n")


with open(FILENAME, "w") as fh:
    json.dump(jaobon_json, fh, indent=4, sort_keys=True)