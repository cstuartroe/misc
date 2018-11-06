import pygame
import time
import math
from threading import Thread
from random import randrange

window_x = 500
window_y = 500

def transparent(color,alpha):
    return tuple(round(channel*alpha) for channel in color)

class Interface:
    def __init__(self, display):
        self.display = display
        self.display.fill((0,0,0))
        self.organisms = []
        self.foods = []
        pygame.display.flip()

    def cls(self):
        self.display.fill((0,0,0))

    def draw(self):
        pass

    def draw_circ(self,color,pos,rad):
        pygame.draw.circle(self.display, color, pos, rad)
        
    def draw_poly(self,color,ptlist):
        pygame.draw.polygon(self.display, color, ptlist)
    
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

def wrap(v):
    return ((v+1)%2)-1

def vecadd(vec1,vec2):
    return tuple(vec1[i]+vec2[i] for i in range(len(vec1)))

def polar(start,rot,rad):
    assert(rot>=-1)
    assert(rot<=1)
    assert(rad>=0)
    # rot doesn't follow normal trig conventions
    # 0 is straight up, negatives to the right, positives to the left
    return (round(math.sin(math.pi*rot)*rad),round(math.cos(math.pi*rot)*rad))

def rot_xy(start,rot,move):
    assert(rot>=-1)
    assert(rot<=1)
    x,y = move
    start_x, start_y = start
    return (start_x + round(x*math.cos(math.pi*rot) - y*math.sin(math.pi*rot)),
            start_y + round(y*math.cos(math.pi*rot) + x*math.sin(math.pi*rot)))

def move_toward(start,target,distance):
    diff = (target[0]-start[0],target[1]-start[1])
    length = (diff[0]**2 + diff[1]**2)**.5
    if length == 0:
        assert(diff == (0,0))
        return start
    return (start[0] + round(diff[0]*distance/length),start[1] + round(diff[1]*distance/length))

def random_pos():
    return (randrange(window_x*100),randrange(window_y*100))

##def random_edge():
##    side = randrange(4)
##    if side == 0:
##        return (randrange(window_x),0)
##    elif side == 1:
##        return (randrange(window_x),window_y)
##    elif side == 2:
##        return (0,randrange(window_y))
##    else:
##        return (window_x,randrange(window_y))

class Organism:
    def __init__(self,interface,ref,i,pos=random_pos(),rot=0,color=randrange(100)):
        self.pos = pos
        self.rot = rot
        self.pos_mom = (0,0)
        self.rot_mom = 0
        self.energy = 5000
        self.color = color_loop(color,100)

        self.ref = ref
        self.i = i
        self.alive = True

        self.interface = interface
        self.draw()

    def draw(self):
        rad = round(self.energy**.5)
        display_pos = (round(self.pos[0]/100)%window_x,round(self.pos[1]/100)%window_y)
        self.interface.draw_circ(self.color,display_pos,rad)
        tailpts = [rot_xy(display_pos,self.rot,(-3,-rad)),
                   rot_xy(display_pos,self.rot,(3,-rad)),
                   rot_xy(display_pos,self.rot,(0,-rad*2))]
        self.interface.draw_poly(self.color,tailpts)

    def iter(self,scoot=False):
        assert(self.alive)
        if scoot:
            self.scoot(1000,0)
        self.friction()
        self.move()

        self.energy -= 1
        if self.energy < 0:
            self.die()
        else:
            self.draw()

    def die(self):
        self.alive = False
        print('I died!')
        del self.ref[self.i]

    def scoot(self,forward,rot_force):
        self.apply_rot_force(rot_force)
        self.apply_pos_force(polar((0,0),self.rot,forward))

    def friction(self):
        self.pos_mom = (self.pos_mom[0]*.98,self.pos_mom[1]*.98)
        self.rot_mom = self.rot_mom*.98

    def move(self):
        self.pos = vecadd(self.pos,self.pos_mom)
        self.rot = wrap(self.rot + self.rot_mom)

    def apply_pos_force(self,force):
        force = (force[0]/self.energy,force[1]/self.energy)
        self.pos_mom = vecadd(self.pos_mom,force)

    def apply_rot_force(self,force):
        self.rot_mom = wrap(self.rot_mom + force)

def evol():
    orgs = []
    org0 = Organism(interface,ref=orgs,i=0)
    orgs.append(org0)
    i = 0
    while True:
        i += 1
        i = i%200
        interface.cls()
        for org in orgs:
            org.iter(i<100)
        pygame.display.flip()

pygame.init()
screen = pygame.display.set_mode((window_x,window_y))
interface = Interface(screen)

t = Thread(target=evol)
t.daemon = True
t.start()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
