from PIL import Image
import numpy as np
import pygame
import pyaudio
from threading import Thread
import cv2
cap = cv2.VideoCapture(0)

pygame.init()
screen = pygame.display.set_mode((512,512))

p = pyaudio.PyAudio()
std_sr = 44100
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=std_sr,
                output=True)

base_freq = 300

def hilbert(n):
    assert(type(n)==int and n>=2)
    if n == 2:
        return np.array([[1,2],[0,3]])
    else:
        base = hilbert(n-1)
        step = 2**(2*(n-2))
        
        ul = base + step
        ur = base + 2*step
        ll = np.rot90(np.flip(base, axis=0))
        lr = base.T + 3*step
        top = np.concatenate((ul,ur),axis=1)
        bottom = np.concatenate((ll,lr),axis=1)
        return np.concatenate((top,bottom),axis=0)

def improcess(im,n):
    im = im.convert('RGB')
    im = im.resize((2**n,2**n))

##    arr = np.array(im)
##    varr = np.vectorize(arr)
##    print(varr)
##    im = Image.fromarray(arr)
    
    x,y = im.size
    for i in range(x):
        for j in range(y):
            r,g,b = im.getpixel((i,j))
            cool = round((g+b)/2)
            im.putpixel((i,j),(r,cool,cool))
    
    im = im.resize((512,512))
    sprite = pygame.image.fromstring(im.tobytes(),im.size,im.mode)
    screen.blit(sprite,sprite.get_rect())
    pygame.display.flip()

def sinewave(volume,sample_rate,duration,freq,func):
    inputs = 2*np.pi*np.arange(sample_rate*duration)*freq/sample_rate
    samples = (volume*func(inputs)).astype(np.float32)
    return samples

def putsine(freq):
    samples = sinewave(.5,std_sr,1,freq,np.sin)
    stream.write(samples)

i = 250

while True:
    for event in pygame.event.get():
        pass
    ret, frame = cap.read()
    #frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    #cp = Image.fromarray(frame)
    #a = improcess(cp,7)
    t = Thread(target=putsine,args=[i])
    t.daemon = True
    t.start()
    i += 1

stream.stop_stream()
stream.close()
p.terminate()
