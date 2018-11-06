import numpy as np
import pyaudio
import random
PyAudio = pyaudio.PyAudio

def sin_wave(amplitude, frequency, duration, bitrate):
    offset = random.random()
    return np.array([amplitude * np.sin((i*frequency/bitrate + offset)*2*np.pi) for i in range(int(duration*bitrate))])

def complex_wave(freq_dict, duration=1, bitrate=44100):
    unscaled = np.zeros(int(duration*bitrate))
    for frequency, amplitude in freq_dict.items():
        unscaled += sin_wave(amplitude, frequency, duration, bitrate)
    max_amplitude = max(max(unscaled),-min(unscaled))
    scaled = (unscaled*(127.5/max_amplitude) + 127.5).astype("int")
    return bytes(list(scaled))

def add_parabola(freq_dict, begin, end, amplitude):
    peak = (((begin-end)/2)**2)
    for x in range(begin+1, end):
        new_value = -amplitude*(x-begin)*(x-end)/peak
        freq_dict[x] = new_value + freq_dict.get(x,0)
    return freq_dict

BITRATE = 44100

p = PyAudio()
stream = p.open(format = p.get_format_from_width(1), 
                channels = 1, 
                rate = BITRATE, 
                output = True)

for i in range(24):
    root = 220*(2**(i/12))
    third = 220*(2**(4*i/12))
    fifth = 220*(2**(7*i/12))
    print(root)
##    freq_dict = add_parabola({}, i, i+10, 1)
    cw = complex_wave({root:1, third:1, fifth:1}, .5, BITRATE)
    stream.write(cw)
    
stream.stop_stream()
stream.close()
p.terminate()
