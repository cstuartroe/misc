from scales import SCALES_31EDO
from scale_info import scale_info
from find_scales import find_canon_rotation, all_subscales

h7n7_family = ["n7 sus pentatonic", "h7 sus pentatonic", "sus bayati pentatonic", "n7 sus hexatonic",
               "n7 major hexatonic",
               "h7 sus hexatonic", "h7 major hexatonic", "n7 heptatonic", "h7 heptatonic", "double 3 heptatonic",
               "double 7 sus heptatonic",
               "double 7 major heptatonic", "double 3 octatonic", "double 7 octatonic", "double 2, 6 nonatonic",
               "double 3, 7 nonatonic", "n7 chromatic"]

theta_family = ["heptatonic theta 1", "heptatonic theta 2", "HSP heptatonic", "h7 heptatonic", "double 3 heptatonic",
                "sub3 heptatonic", "chromatic theta"]

modified_dioudeteric_family = ["heptatonic H", "double 6 sub2 n7 heptatonic", "sub2 h7 heptatonic",
                               "double 3 tritone h7 heptatonic", "double 7 major heptatonic",
                               "double 3 no 4 h7 heptatonic", "aug4 subphrygian h7 heptatonic",
                               "double 2 aug4 sus h7 heptatonic", "double 2 no 4 h7 heptatonic",
                               "aug4 h7 heptatonic", "sub3 up4 sub6 n7 heptatonic", "up4 double 7 sus heptatonic",
                               "sub3 no 4 sub6 double 7 heptatonic",
                               "double 3 no 4 double 6 no 7 heptatonic", "up4 no 6 double 7 heptatonic",
                               "neutral diatonic", "2,6 dioudeteric modified dodecatonic"]

god_B_family = ["sub3 heptatonic", "HSP heptatonic", "double 2 dim5 sus heptatonic", "double 2 no 5  major heptatonic",
                "heptatonic D", "heptatonic F", "aug4 subphrygian h7 heptatonic", "god chromatic B"]


def find_subscales(scale, priorities_function, length):
    subscales = []
    for subscale in all_subscales(scale, length):
        subscales.append((subscale, *priorities_function(subscale)))

    subscales.sort(key=lambda x: x[1:])
    print(len(subscales))
    for subscale_stats in subscales:
        this_scale_names = []
        for scale_name, named_scale in SCALES_31EDO.items():
            if tuple(find_canon_rotation(named_scale)) == subscale_stats[0]:
                this_scale_names.append(scale_name)
        print(*subscale_stats, *this_scale_names)


if __name__ == "__main__":
    for scale_name in modified_dioudeteric_family:
        scale_info(scale_name)

    # find_subscales(SCALES_31EDO["chromatic theta"], dioudeteric_priorities, 7)
    # find_subscales(SCALES_31EDO["2,6 dioudeteric modified dodecatonic"], unknown_priorities, 9)
