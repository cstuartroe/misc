NOTES_12_EDO = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def get_12_edo_name(midi_number):
    letter = NOTES_12_EDO[midi_number % 12]
    octave = (midi_number//12) - 1
    return f"{letter}{octave}"
