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


if os.path.exists(FILENAME):
    with open(FILENAME, "r") as fh:
        jaobon_json = json.load(fh)
else:
    jaobon_json = {"roots": {}, "invalid_roots": {}}


if "makesylls" in sys.argv:
    syllables = set()

    for f in FINALS:
        syllables.add(f)
        for o in ONSETS:
            syll = o + f
            if all(s not in syll for s in FORBIDDEN_SEQUENCES):
                syllables.add(syll)

    print(len(syllables), "syllables possible.")

    for syll in syllables:
        if syll not in jaobon_json["roots"]:
            if syll in jaobon_json["invalid_roots"]:
                jaobon_json["roots"][syll] = jaobon_json["invalid_roots"][syll]
                del jaobon_json["invalid_roots"][syll]
            else:
                jaobon_json["roots"][syll] = None

    for syll in list(jaobon_json["roots"].keys()):
        if syll not in syllables:
            jaobon_json["invalid_roots"][syll] = jaobon_json["roots"][syll]
            del jaobon_json["roots"][syll]

    num_defns = len([d for d in jaobon_json["roots"].values()
                    if d is not None])
    print(f"{num_defns} definitions set.")

    with open(FILENAME, "w") as fh:
        json.dump(jaobon_json, fh, indent=4, sort_keys=True)


elif "csv" in sys.argv:
    sorted_sylls = sorted(list(jaobon_json["roots"].items()), key=lambda x: x[0])
    with open("sylls.csv", "w") as fh:
        for syll, defn in sorted_sylls:
            fh.write(f"{syll}\t{defn or '...'}\n")
