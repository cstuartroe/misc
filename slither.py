import pygame
import time
import math
from threading import Thread
from random import randrange

global window_x
global window_y

def transparent(color,alpha):
    return tuple(round(channel*alpha) for channel in color)

class Interface:
    def __init__(self, display):
        self.display = display
        self.display.fill((0,0,0))
        pygame.display.flip()

    def cls(self):
        self.display.fill((0,0,0))
           
    def draw_circs(self,circs,refresh = True):
        if refresh:
            self.cls()
        self.draw_circ_layer(circs,1,10)
##        self.draw_circ_layer(circs,.4,9)
##        self.draw_circ_layer(circs,.6,8)
##        self.draw_circ_layer(circs,.8,6)
##        self.draw_circ_layer(circs,1,4)
        pygame.display.flip()

    def draw_circ_layer(self,circs,alpha,rad):
        for circ in circs:
            color, dims = circ
            x, y = dims
            pygame.draw.circle(self.display, transparent(color,alpha), (x,y), rad)        

def color_loop(i,l):
    red = round((math.sin(i/l)+1)*127)
    green = round((math.sin((i-(2*l))/l)+1)*127)
    blue = round((math.sin((i-(4*l))/l)+1)*127)
    return (red,green,blue)

def dist(pos1,pos2):
    return ((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)**.5

def move_toward(start,target,distance):
    diff = (target[0]-start[0],target[1]-start[1])
    length = (diff[0]**2 + diff[1]**2)**.5
    if length == 0:
        assert(diff == (0,0))
        return start
    return (start[0] + round(diff[0]*distance/length),start[1] + round(diff[1]*distance/length))

def random_pos():
    return (randrange(window_x),randrange(window_y))

def random_edge():
    side = randrange(4)
    if side == 0:
        return (randrange(window_x),0)
    elif side == 1:
        return (randrange(window_x),window_y)
    elif side == 2:
        return (0,randrange(window_y))
    else:
        return (window_x,randrange(window_y))

class Drifter:
    def __init__(self):
        #self.pos = random_pos()
        self.pos = window_x//2, window_y//2
        self.i = randrange(360)
        self.momentum = (randrange(-6,7),randrange(-6,7))

    def get_circ(self):
        self.momentum = (self.momentum[0] + randrange(-1,2), self.momentum[1] + randrange(-1,2))
        self.momentum = move_toward((0,0),self.momentum,10)
        self.pos = ((self.pos[0] + self.momentum[0])%window_x,
                    (self.pos[1] + self.momentum[1])%window_y)
        self.i += 1
        return (color_loop(self.i,100),self.pos)

def snake():
    loop_length = 100
    circs = [(color_loop(i,loop_length),(i*10,100)) for i in range(50)]
    apple = ((255,255,255),random_edge())
    circs += [apple]
    i = 50
    while True:
        for event in pygame.event.get():
            pass
        #x = pygame.mouse.get_pos()
        x = apple[1]
        mouse_dist = dist(circs[-2][1],x)
        if mouse_dist >= 1:
            i += 1
            new_pos = move_toward(circs[-2][1],x,min(10,mouse_dist))
            apple_dist = dist(apple[1],new_pos)
            if apple_dist < 20:
                old_apple = apple
                apple = ((255,255,255),random_edge())
                circs = circs[:-1] + [(color_loop(i,loop_length),new_pos)] + [apple]
            else:
                circs = circs[1:-1] + [(color_loop(i,loop_length),new_pos)] + [apple]
            interface.draw_circs(circs)
        #time.sleep(.001)

def drift():    
    while True:
        drifters = [Drifter() for i in range(25)]
        for i in range(10000):
            interface.draw_circs([d.get_circ() for d in drifters],False)
            time.sleep(.01)
        interface.cls()

##prompt = """Which experience do you want?
##    1 = snake
##    2 = drift
##"""
##experiences = {'1':snake,'2':drift}
##target = experiences[input(prompt)]

pygame.init()
screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
window_x, window_y = screen.get_size()
interface = Interface(screen)

t = Thread(target=drift)
t.daemon = True
t.start()
