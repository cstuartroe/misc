import numpy as np
from PIL import Image, ImageTk
import sounddevice as sd
from tkinter import Tk, Canvas, NW, Label, PhotoImage
import random
import time
from threading import Thread

root = Tk()
canvas = Canvas(root, width=1200, height=720)
canvas.pack()

fs = 44100
duration = .01  # seconds

z = np.zeros((720, 1200))
current_volume = 0


class Timer:
    def __init__(self):
        self.actions = {}
        self.current_action = None
        self.current_start_time = 0
        self.loops = 0

    def loop(self):
        self.loops += 1

    def start(self, action_name):
        if self.current_action:
            self.stop()

        self.current_action = action_name
        self.current_start_time = time.time()

    def stop(self):
        self.actions[self.current_action] = self.actions.get(self.current_action, 0) + (time.time() - self.current_start_time)
        self.current_action = None

    def printout(self):
        print(f"{self.loops} loops")
        for action_name, time_elapsed in self.actions.items():
            print(action_name.ljust(20, " "), f"{round(time_elapsed, 3)}s")

visual_timer = Timer()
audio_timer = Timer()


def update_current_volume(indata):
    global current_volume
    current_volume = np.average(np.abs(indata))


def audio_callback(indata, outdata, frames, time, status):
##    audio_timer.loop()
##    audio_timer.start("threading")
    Thread(target=update_current_volume, args=(indata,)).start()
##    audio_timer.stop()

def animate():
    visual_timer.loop()

    visual_timer.start("Image render")
    img = Image.fromarray(np.uint8((current_volume+z)*2*255), "L")
    root.render = ImageTk.PhotoImage(img)

    visual_timer.start("Painting")
    canvas.create_image(0, 0, anchor=NW, image=root.render)
##        root.l = Label(root, image=root.render).pack(side="left")
    visual_timer.stop()
    
    root.after(1, animate)


animate()
root.after(10000, visual_timer.printout)
##root.after(10000, audio_timer.printout)


stream = sd.Stream(
        channels=2,
        samplerate=44100, callback=audio_callback)

with stream:
    root.mainloop()



##chunk = 1024  # Record in chunks of 1024 samples
##sample_format = pyaudio.paInt16  # 16 bits per sample
##seconds = 3
##
##input_device_index = 0
##p = pyaudio.PyAudio()  # Create an interface to PortAudio
##filename = f"output{input_device_index}.wav"
##info = p.get_device_info_by_index(input_device_index)
##fs = int(info['defaultSampleRate'])
##channels = 1 # info["maxOutputChannels"]
##
##print(f'Recording {input_device_index}')
##
##stream = p.open(format=sample_format,
##                channels=channels,
##                rate=fs,
##                frames_per_buffer=chunk,
##                input=True,
##                input_device_index=6)
##
##frames = []  # Initialize array to store frames
##
### Store data in chunks for 3 seconds
##for i in range(0, int(fs / chunk * seconds)):
##    data = stream.read(chunk, exception_on_overflow=False)
##    frames.append(data)
##
### Stop and close the stream 
##stream.stop_stream()
##stream.close()
### Terminate the PortAudio interface
##p.terminate()
##
### Save the recorded data as a WAV file
##wf = wave.open(filename, 'wb')
##wf.setnchannels(channels)
##wf.setsampwidth(p.get_sample_size(sample_format))
##wf.setframerate(fs)
##wf.writeframes(b''.join(frames))
##wf.close()
