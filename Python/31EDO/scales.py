DEGREES_24EDO = [
  "unison", 
  "sub2",
  "m2",
  "n2",
  "maj2",
  "sup2/sub3",
  "m3",
  "n3",
  "maj3",
  "sup3/down4",
  "4",
  "up4",
  "aug4/dim5",
  "down5",
  "5",
  "up5/sub6",
  "m6",
  "n6",
  "maj6",
  "sup6/h7",
  "m7",
  "n7",
  "maj7",
  "sup7",
  "octave"
]

DEGREES_31EDO = [
  "unison",
  "step",
  "sub2",
  "m2",
  "n2",
  "maj2",
  "sup2",
  "sub3",
  "m3",
  "n3",
  "maj3",
  "sup3/dim4",
  "down4",
  "4",
  "up4",
  "aug4",
  "dim5",
  "down5",
  "5",
  "up5",
  "aug5/sub6",
  "min6",
  "n6",
  "maj6",
  "sup6",
  "h7",
  "min7",
  "n7",
  "maj7",
  "sup7",
  "sub8",
  "octave"
]

SCALES_31EDO = {
  "diatonic": [5, 5, 3, 5, 5, 5, 3],
  "12-TET approx": [3, 2, 3, 2, 3, 3, 2, 3, 2, 3, 2, 3],
  "neutral diatonic": [4, 4, 5, 4, 4, 5, 5],
  "neutral": [4, 4, 5, 4, 5, 4, 5],
  "hahn symmetric pentachordal": [3, 3, 4, 3, 5, 3, 4, 3, 3],
  "HSP heptatonic": [3, 7, 3, 5, 3, 7, 3],
  "hahn neutral": [3, 3, 3, 4, 5, 3, 3, 3, 4],
  "hahn nonatonic": [4, 4, 2, 5, 3, 3, 4, 3, 3],
  
  "strange decatonic": [3, 2, 3, 2, 3, 4, 4, 2, 4, 4],
  "god nonatonic": [5, 5, 3, 2, 3, 5, 3, 2, 3],
  "sub3 heptatonic": [7, 3, 3, 5, 2, 8, 3],

  "heptatonic B": [5, 5, 3, 5, 5, 6, 2],
  "heptatonic D": [5, 5, 3, 3, 2, 5, 8],
  "heptatonic E": [4, 6, 3, 5, 5, 5, 3],
  "heptatonic F": [6, 4, 3, 5, 5, 5, 3],
  "heptatonic G": [6, 5, 4, 4, 5, 5, 2],
  "heptatonic H": [5, 5, 4, 4, 5, 2, 6],
  "nonatonic I": [3, 2, 5, 3, 5, 3, 2, 4, 4],
  "dodecatonic A": [3, 3, 3, 2, 2, 3, 3, 2, 3, 2, 3, 2],
  "dodecatonic B": [3, 3, 3, 2, 3, 2, 3, 2, 3, 3, 2, 2],
  "dodecatonic C": [3, 3, 3, 2, 2, 3, 3, 2, 3, 3, 2, 2],
  "dodecatonic D": [3, 2, 2, 4, 2, 3, 2, 3, 2, 2, 4, 2],
  "dodecatonic E": [4, 2, 2, 3, 2, 4, 2, 2, 3, 2, 3, 2],
  "dodecatonic F": [4, 2, 3, 2, 2, 3, 3, 3, 2, 3, 2, 2],
  "dodecatonic G": [4, 2, 2, 3, 2, 3, 3, 3, 2, 2, 3, 2],
 
  "n7 sus pentatonic": [5, 8, 5, 9, 4],
  "h7 sus pentatonic": [5, 8, 5, 7, 6],
  "sus bayati pentatonic": [5, 8, 5, 4, 9],
  "n7 sus hexatonic": [5, 8, 5, 5, 4, 4],
  "n7 major hexatonic": [5, 5, 8, 5, 4, 4],
  "h7 sus hexatonic": [5, 8, 5, 5, 2, 6],
  "h7 major hexatonic": [5, 5, 8, 5, 2, 6],
  "n7 heptatonic": [5, 5, 3, 5, 5, 4, 4],
  "h7 heptatonic": [5, 5, 2, 6, 5, 5, 3],
  "double 3 heptatonic": [5, 2, 3, 3, 5, 5, 8],
  "double 7 sus heptatonic": [5, 8, 5, 5, 2, 2, 4],
  "double 7 major heptatonic": [5, 5, 8, 5, 2, 2, 4],
  "double 3 octatonic": [5, 2, 3, 3, 5, 5, 4, 4],
  "double 7 octatonic": [5, 5, 3, 5, 5, 2, 2, 4],
  "double 2, 6 nonatonic": [2, 3, 5, 3, 5, 2, 3, 4, 4],
  "double 3, 7 nonatonic": [5, 2, 3, 3, 5, 5, 2, 2, 4],
  "n7 chromatic": [2, 3, 2, 3, 3, 2, 3, 2, 3, 2, 2, 4],
  
  "3,7 dioudeteric dodecatonic": [3, 2, 3, 2, 4, 2, 2, 3, 2, 2, 2, 4],
  "3,7 dioudeteric decatonic": [3, 2, 3, 2, 4, 4, 3, 2, 4, 4],
  "3,7 functional dioudeteric nonatonic": [5, 3, 2, 4, 4, 3, 2, 4, 4],
  "3,7 colorful dioudeteric nonatonic": [3, 2, 5, 4, 4, 3, 2, 4, 4],
  
  "2,6 dioudeteric dodecatonic": [2, 3, 2, 3, 4, 2, 2, 2, 3, 2, 2, 4],
  "2,6 dioudeteric decatonic": [2, 3, 2, 3, 4, 4, 2, 3, 4, 4],
  "2,6 functional dioudeteric nonatonic": [2, 3, 5, 4, 4, 2, 3, 4, 4],
  "2,6 colorful dioudeteric nonatonic": [5, 2, 3, 4, 4, 2, 3, 4, 4],
 
  "2,6 dioudeteric modified dodecatonic": [2, 3, 2, 3, 4, 1, 3, 2, 3, 2, 2, 4],
  "double 6 sub2 n7 heptatonic": [2, 8, 8, 2, 3, 4, 4],
  "sub2 h7 heptatonic": [2, 8, 5, 3, 5, 2, 6],
  "double 3 tritone h7 heptatonic": [2, 5, 3, 5, 8, 2, 6],
  "double 2 aug4 sus h7 heptatonic": [2, 3, 10, 3, 5, 2, 6],
  "double 2 no 4 h7 heptatonic": [2, 3, 5, 8, 5, 2, 6],
  "aug4 h7 heptatonic": [5, 5, 5, 3, 5, 2, 6],
  "double 3 no 4 h7 heptatonic": [5, 2, 3, 8, 5, 2, 6],
  "aug4 subphrygian h7 heptatonic": [2, 5, 8, 3, 2, 5, 6],
  "up4 no 6 double 7 heptatonic": [5, 2, 7, 4, 7, 2, 4],
  "double 3 no 4 double 6 no 7 heptatonic": [2, 5, 3, 8, 2, 3, 8],
  "sub3 no 4 sub6 double 7 heptatonic": [5, 2, 11, 2, 5, 2, 4],
  "up4 double 7 sus heptatonic": [7, 7, 4, 2, 5, 2, 4],
  "sub3 up4 sub6 n7 heptatonic": [5, 2, 7, 4, 2, 7, 4],

  "plain pentatonic": [8, 5, 5, 8, 5],
  "3,7 super pentatonic": [7, 5, 6, 7, 6],
  "2,6 super pentatonic": [6, 5, 7, 6, 7],

  "nonatonic alpha": [7, 2, 8, 1, 2, 2, 5, 3, 1],
  "nonatonic beta": [7, 2, 8, 1, 2, 5, 2, 3, 1],
  "nonatonic gamma": [8, 2, 7, 1, 3, 2, 5, 2, 1],
  "nonatonic delta": [8, 2, 7, 1, 3, 5, 2, 2, 1],

  # interval_diversity({7, 25}) chord_richness([7,8,10]) mmaj fifths
  # 2 4 10 10
  "chromatic alpha": [2, 3, 5, 2, 3, 2, 1, 5, 2, 3, 2, 1],
  "chromatic beta": [3, 2, 3, 2, 5, 1, 2, 3, 2, 5, 1, 2],
  # 2 4 12 10
  "chromatic gamma": [3, 2, 3, 2, 5, 1, 2, 3, 2, 3, 2, 3],
  "chromatic delta": [2, 3, 2, 3, 2, 6, 2, 3, 2, 3, 2, 1],
  "chromatic epsilon": [5, 2, 3, 2, 3, 3, 2, 3, 2, 3, 2, 1],
  "chromatic zeta": [2, 3, 2, 3, 2, 3, 3, 5, 2, 3, 2, 1],
  # 2 4 13 9
  "chromatic eta": [5, 2, 3, 5, 2, 1, 2, 3, 2, 3, 2, 1],
  "chromatic iota": [2, 3, 2, 3, 5, 2, 1, 5, 2, 3, 2, 1],
  "chromatic kappa": [5, 2, 3, 3, 2, 2, 1, 2, 3, 5, 2, 1],
  "chromatic lambda": [5, 2, 3, 3, 2, 3, 2, 3, 2, 3, 2, 1],
  # 2 5 10 10
  "chromatic mu": [3, 2, 3, 2, 1, 5, 2, 3, 2, 5, 1, 2],
  "chromatic nu": [5, 2, 3, 2, 3, 2, 1, 5, 2, 3, 2, 1],
  # 2 5 11 7
  "chromatic xi": [5, 2, 1, 7, 1, 2, 3, 4, 1, 2, 1, 2],
  "chromatic omicron": [3, 5, 2, 1, 2, 5, 2, 1, 3, 4, 1, 2],
  # 2 5 11 9
  "chromatic pi": [4, 1, 2, 3, 2, 3, 2, 1, 5, 2, 3, 3],
  "chromatic rho": [4, 1, 2, 3, 5, 2, 1, 5, 2, 3, 2, 1],

  "chromatic theta": [2, 3, 2, 3, 3, 5, 2, 3, 3, 2, 2, 1],
  "heptatonic theta 1": [5, 5, 3, 5, 5, 7, 1],
  "heptatonic theta 2": [5, 5, 2, 1, 5, 5, 8],

  "god chromatic A": [2, 3, 4, 1, 3, 2, 3, 2, 3, 3, 1, 4],

  "god chromatic B": [3, 2, 4, 1, 3, 3, 2, 3, 2, 3, 1, 4],
  "double 2 dim5 sus heptatonic": [3, 2, 8, 3, 7, 3, 5],
  "double 2 no 5  major heptatonic": [3, 2, 5, 3, 8, 2, 8],

  "proper nonatonic A": [4, 1, 5, 3, 5, 2, 3, 5, 3],
  "proper nonatonic B": [5, 1, 4, 3, 5, 3, 2, 5, 3],
  "strictly proper nonatonic A": [3, 3, 3, 4, 3, 3, 5, 2, 5],
  "strictly proper nonatonic B": [5, 2, 5, 3, 3, 4, 3, 3, 3],

  "melodic god B heptatonic": [5, 8, 3, 2, 4, 1, 8],

  "ultra melodic heptatonic": [5, 5, 6, 2, 1, 4, 8],
  "melodic octatonic 27 A": [6, 4, 1, 5, 8, 4, 1, 2],
  "melodic octatonic 27 B": [6, 4, 1, 5, 3, 5, 5, 2],
  "melodic dodecatonic 27": [5, 1, 4, 1, 5, 2, 1, 4, 1, 4, 1, 2],

  "melodic octatonic 31 A": [3, 2, 7, 1, 3, 2, 8, 5],
  "melodic octatonic 31 B": [3, 5, 5, 3, 5, 2, 3, 5],
  "ultra melodic nonatonic": [5, 3, 4, 1, 5, 3, 2, 3, 5],
  "melodic dodecatonic 31": [3, 2, 3, 4, 1, 3, 2, 3, 2, 2, 1, 5],

  "no-step melodic nonatonic": [5, 3, 5, 2, 3, 4, 4, 3, 2],
  "no-step melodic dodecatonic": [3, 3, 2, 3, 2, 4, 2, 2, 3, 2, 3, 2],

  "harmonic 7 near-diatonic": [6, 6, 2, 5, 5, 5, 2],

  "septimal playground diatonic": [5, 5, 2, 6, 5, 5, 3],
  "septimal playground octatonic 1": [5, 5, 2, 3, 3, 5, 5, 3],
  "septimal playground octatonic 2": [5, 3, 2, 2, 6, 5, 5, 3],
  "septimal playground nonatonic 1": [5, 3, 2, 2, 3, 3, 5, 5, 3],
  "septimal playground nonatonic 2": [5, 3, 2, 2, 6, 3, 2, 5, 3],
  "septimal playground decatonic":   [5, 3, 2, 2, 3, 3, 3, 2, 5, 3],
  "septimal playground chromatic": [3, 2, 3, 2, 2, 3, 3, 3, 2, 3, 2, 3],

  "consonant heptatonic": [5, 3, 5, 5, 5, 6, 2],
  "consonant hexatonic": [5, 8, 5, 5, 6, 2],

  "fairly consonant many-chorded octatonic": [7, 3, 3, 5, 2, 3, 5, 3],
  "consonant octatonic A": [5, 5, 3, 5, 2, 6, 2, 3],
  "consonant octatonic B": [5, 2, 3, 3, 5, 5, 5, 3],
}

SCALES_24EDO = {
  "dioudeteric decatonic": [3, 3, 2, 2, 2, 2, 3, 3, 2, 2],
  "functional dioudeteric nonatonic": [3, 3, 2, 2, 4, 3, 3, 2, 2],
  "colorful dioudeteric nonatonic": [3, 3, 4, 2, 2, 3, 3, 2, 2],
  "neutral heptatonic": [3, 3, 4, 4, 3, 3, 4],
  "plain pentatonic": [6, 4, 4, 6, 4],
  "super pentatonic": [5, 4, 5, 5, 5]
}

SCALE_REFS = {
  24: SCALES_24EDO,
  31: SCALES_31EDO
}

DEGREE_REFS = {
  24: DEGREES_24EDO,
  31: DEGREES_31EDO
}

TETRACHORDS_31EDO = {
  "h7": (10, 18, 25),
  "dom7": (10, 18, 26),
  "m7": (8, 18, 26),
  "maj7": (8, 18, 28),
  "subminadd4": (7, 13, 18),
  "subminmaj7": (7, 18, 28),
  "minmaj7": (8, 18, 28),
}