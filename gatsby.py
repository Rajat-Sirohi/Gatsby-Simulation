import pygame
import random
from math import sqrt
import numpy as np
import matplotlib.pyplot as plt


##############
# INITIALIZE #
##############
black = (0,0,0)
white = (255,255,255)

dispWidth = 1000
dispHeight = 1000

n = 100
maxRadius = 80
pos = 0
fig = plt.figure()
percInfl = .50

inflFactor = 0.3
despFactor = 0.3
hopeFactor = 0.3

inflList = [0]
despList = [0]
hopeList = [0]

##########
# PERSON #
##########
class Person():
    def __init__(self, influence, desperation, hope):
        self.influence = influence
        self.desperation = desperation
        self.hope = hope

        self.collide = False
        
        self.color = (self.influence/100*255, self.desperation/100*255, self.hope/100*255)
        self.radius = (int)(10+(maxRadius-10)*self.influence/100)

        self.vel = pygame.math.Vector2(0,0)
        self.vel.x = random.uniform(-30, 30)
        self.vel.y = random.uniform(-30, 30)
        
        self.pos = pygame.math.Vector2(0,0)
        self.pos.x = random.randint(.1*dispWidth, .9*dispWidth)
        self.pos.y = random.randint(.1*dispHeight, .9*dispHeight)

    def update(self, dt, people):
        self.pos.x += self.vel.x*dt
        if self.pos.x-self.radius < 0 or self.pos.x+self.radius > dispWidth:
            self.vel.x*=-1
            if self.pos.x-self.radius < 0:
                self.pos.x = self.radius
            if self.pos.x+self.radius > dispWidth:
                self.pos.x = dispWidth-self.radius
                
        self.pos.y += self.vel.y*dt
        if self.pos.y-self.radius < 0 or self.pos.y+self.radius > dispHeight:
            self.vel.y*=-1
            if self.pos.y-self.radius < 0:
                self.pos.y = self.radius
            if self.pos.y+self.radius > dispHeight:
                self.pos.y = dispHeight-self.radius

        if (self.influence > 50):
            for p in people:
                if (p.influence < 50):
                    d = sqrt((self.pos.x-p.pos.x)**2+(self.pos.y-p.pos.y)**2)
                    if (d < self.radius+p.radius) and not self.collide and not p.collide:
                        self.influence += inflFactor*(100-self.influence)
                        p.desperation += despFactor*(100-p.desperation)
                        p.hope += hopeFactor*(100-p.hope)
                        
                        self.radius = (int)(10+(maxRadius-10)*self.influence/100)
                        p.radius = (int)(.85*(10+(maxRadius-10)*(p.desperation+p.hope)/5/100))

                        self.collide = True
                        p.collide = True


#######
# RUN #
#######
def run():
    global pos, inflList, despList, hopeList
    
    pygame.init()
    display = pygame.display.set_mode((dispWidth, dispHeight))
    clock = pygame.time.Clock()
    gameExit = False
    speedFactor = 50
    
    people = []
    for i in range(n):
        # % chance for protestant
        if (random.random() <= percInfl):
            people.append(Person(random.randint(50,75), 0, 0))
        else:
            people.append(Person(0, random.randint(50,75), random.randint(50,75)))
            
    while not gameExit:
        dt = clock.tick(60)/speedFactor
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
                pygame.image.save(display, "game.jpg")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    speedFactor += 3
                if event.key == pygame.K_RIGHT:
                    speedFactor -= 3
                    
        display.fill(black)
        for p in people:
            pygame.draw.circle(display, p.color, ((int)(p.pos.x), (int)(p.pos.y)), p.radius)
            p.update(dt, people)
            
            if (p.influence > 50):
                inflList[pos] = .5*(inflList[pos]+p.influence)
            if (p.desperation > 50):
                despList[pos] = .5*(despList[pos]+p.desperation)
            if (p.hope > 50):
                hopeList[pos] = .5*(hopeList[pos]+p.hope)

        if (pos%10 == 0):
            for p in people:
                p.collide = False
                time = 0
                
        pygame.display.update()
        clock.tick(60)
        
        if (pos%50 == 0):
            plot()

        pos += 1
        inflList.append(0)
        despList.append(0)
        hopeList.append(0)

def plot():
    global inflList, despList, hopeList, pos

    plt.plot(inflList, label='Influence', color=(1,0,0))
    plt.plot(despList, label='Desperation', color=(0,1,0))
    plt.plot(hopeList, label='Hope', color=(0,0,1))

    if pos==0:
        plt.legend()
    plt.draw()
    plt.pause(0.05)

run()
pygame.quit()
quit()

plt.show()
