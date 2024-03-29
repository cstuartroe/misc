import random
import pygame
import time
import numpy as np
import math

pygame.init()
screen = pygame.display.set_mode((1200,612))

def x2rgb(value):
    return tuple(int(value[i: i+2], 16) for i in range(1,7,2))

class Plot:
    def __init__(self):
        self.x_size = 100
        self.y_size = 51
        self.build_grid()
        self.interface = Interface(screen)
        self.build_interface()
        self.rounds = 0
        self.winning_genomes = []
        self.winning_ages = []
        self.time = pygame.time.get_ticks()
        self.skip = 10
        
        self.worms = []
        for i in range(self.y_size//4):
            worm = Worm(random_genome())
            worm.set_master(self,i*4+3,i)
            self.worms.append(worm)

        while True:
            self.loop()

    def build_grid(self):
        self.grid = [[('rockboi' if random.randrange(30) == 0 else 'nada') for x in range(self.x_size)] for y in range(self.y_size)]

    def get_grid_value(self,x,y):
        if 0<=x and x<self.x_size and 0<=y and y<self.y_size:
            return self.grid[y][x]
        else:
            return 'wall'

    def set_grid_value(self,x,y,value):
        self.grid[y][x] = value
        self.interface.draw_square(x,y,value)

    def build_interface(self):
        for x in range(100):
            for y in range(51):
                self.interface.draw_square(x,y,self.grid[y][x])
        pygame.display.flip()

    def print_time(self):
        newtime = pygame.time.get_ticks()
        print(newtime - self.time)
        self.time = newtime

    def loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        pygame.event.clear()                
        if len(self.winning_genomes) < 4:
            self.move()
        else:
            self.rounds += 1
            print('Winner of round %s is' % (str(self.rounds)))
            print(self.winning_genomes[0])
            print('at age %s.' % self.winning_ages[0])
            self.build_grid()
            self.build_interface()
            self.worms = []
            for i in range(4):
                for j in range(4):
                    if i != j:
                        first_genome = self.winning_genomes[i]
                        second_genome = self.winning_genomes[j]
                        genome = [(first_genome[i] + second_genome[i])/2 for i in range(len(first_genome))]
                        self.worms.append(Worm(genome))
            for i in range(12):
                self.worms[i].set_master(self,i*4+3,i)
            self.winning_genomes = []
            self.winning_ages = []
            
        pygame.display.flip()
        pygame.time.wait(self.skip)

    def move(self):
        for worm in self.worms:
            worm.decide()

    def record_winner(self,worm):
        self.winning_genomes += [worm.genome]
        self.winning_ages += [worm.lifespan]

class Interface:
    def __init__(self, display):
        self.display = display
        self.pallette = {'nada':'#000000','rockboi':'#888888','worm':'#00ff00'}
        self.display.fill((0,0,0))
        pygame.display.flip()
           
    def draw_square(self,x,y,content):
        pygame.draw.rect(self.display, x2rgb(self.pallette[content]), (x*12,y*12,11,11))
        
def random_genome():
    return [(random.random() - .5)*3 for i in range(16)]

def sigmoid(x):
    return 2/(1 + math.e**(-x)) - 1

class Worm:
    def __init__(self,genome):
        self.genome = genome
        self.directions = {0:(1,0),1:(0,1),2:(-1,0),3:(0,-1)}
        self.direction = 0
        self.recur = 0
        self.lifespan = 0
        self.paused = 0
        self.build_brain()

    def build_brain(self):
        self.synapses1 = [[self.genome[0],self.genome[1]],[self.genome[2],self.genome[3]],[self.genome[4],self.genome[5]]]
        self.synapses2 = [[self.genome[6],self.genome[7],self.genome[8]],[self.genome[9],self.genome[10],self.genome[11]],\
                          [self.genome[12],self.genome[13],self.genome[14]]]
        self.mutation_rate = self.genome[15]

    def set_master(self,master,y,index):
        self.master = master
        self.index = index
        self.reset_segments(y)

    def reset_segments(self,y):
        self.direction = 0
        self.segments = [(i,y) for i in range(4)]
        for segment in self.segments:
            self.draw_segment(segment)

    def draw_segment(self,segment):
        self.master.set_grid_value(segment[0],segment[1],'worm')

    def erase_segment(self,segment):
        self.master.set_grid_value(segment[0],segment[1],'nada')

    def see(self):
        head = self.segments[-1]
        delta = self.directions[self.direction]
        for i in range(1,self.master.x_size + 1):
            sight = self.master.get_grid_value(head[0] + delta[0]*i, head[1] + delta[1]*i)
            if sight != 'nada':
                return i
        print(delta)
        print(head)
        global err
        err = self.master.grid
        raise TypeError('how the fuck did we get here?')

    def decide(self):
        self.lifespan += 1
        self.mutate()
        
##        if self.lifespan % 5000 == 0:
##            print(self.lifespan)
##            print(self.genome)
            
        inputs = [[1,self.see(),self.recur]]

        try:
            midlayer = np.dot(inputs,self.synapses1)
            midlayer = [[1] + [sigmoid(x) for x in midlayer[0]]]
        except TypeError:
            print(inputs)
            print(self.synapses1)

        outputs = np.dot(midlayer,self.synapses2)
        outputs = [sigmoid(x) for x in outputs[0]]

        direction = round(outputs[0])
        distance = 1 if outputs[1] < 0 else 2
        self.recur = outputs[2]
        
        self.move(direction,distance)

    #turn: -1 = left, 0 = straight, 1 = right
    #distance: 1 or 2
    def move(self,turn,distance):
        self.direction = (self.direction + turn) % 4
        for i in range(distance):
            head = self.segments[-1]
            delta = self.directions[self.direction]
            ahead_position = (head[0]+delta[0],head[1]+delta[1])
            ahead_object = self.master.get_grid_value(ahead_position[0],ahead_position[1])
            if ahead_object == 'nada':
                self.paused = 0
                self.erase_segment(self.segments[0])
                self.segments = self.segments[1:] + [ahead_position]
                self.draw_segment(self.segments[-1])
            else:
                self.paused += 1
        if self.paused >= 1000:
            self.paused = 0
            for segment in self.segments:
                self.erase_segment(segment)
            new_y = random.randrange(self.master.y_size)
            self.reset_segments(new_y)
        if self.segments[-1][0] == self.master.x_size - 1:
            for segment in self.segments:
                self.erase_segment(segment)
            self.reset_segments(random.randrange(self.master.y_size))
            self.master.record_winner(self)
            self.lifespan = 0

    def mutate(self):
        newgenome = []
        for value in self.genome:
            firstrand = random.random()
            secondrand = random.random()
            newgene = round((value * (1 + (firstrand - .5)*(self.mutation_rate))) + (secondrand - .5)*(.001 * math.log(self.lifespan)),3)
            if newgene == 0:
                newgene = .001
            elif abs(newgene) > 100:
                newgene = newgene/100
            newgenome += [newgene]
        self.genome = newgenome
        self.build_brain()

    def mate(self,other):
        genome = [(self.genome[i] + other.genome[i])/2 for i in range(len(self.genome))]
        return Worm(genome)

if __name__ == "__main__":
    p = Plot()
