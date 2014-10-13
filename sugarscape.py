'''
Created on 2010-04-17

@author: rv
'''

import pygame
from pygame.locals import *
import random
from itertools import product
from environment import Environment
from agent import Agent
from wdgPopulation import WdgPopulation
from wdgWealth import WdgWealth
from wdgAgent import WdgAgent

''' 
initial simulation parameters
'''

# view
screenSize = 600, 600
colorBackground = 250,250,250

colorSugar = ((250,250,220),
              (250,250,200),
              (250,250,180),
              (250,250,160),
              (250,250,140),
              (250,250,120),
              (250,250,100),
              (250,250,80),
              (250,250,60),
              (250,250,40))

colorRed = 250, 50, 50
colorPink = 250, 50, 250
colorBlue = 50, 50, 250
fps = 10

# environment
gridSize = 50, 50
northSite = 40, 10, 20
southSite = 15, 35, 20
maxCapacity = 10
seasonPeriod = 50
northRegion = 0, 0, 49, 24
southRegion = 0, 25, 49, 49
growFactor = 1
growFactor1 = 1
growFactor2 = float(growFactor1) / 8

# agents
# agentColorScheme: Agents colour meaning = 0:all, 1:bySexe, 2:byMetabolism, 3:byVision, 4:byGroup
maxAgentMetabolism = 4
maxAgentVision = 6
initEndowment = 50, 100
minmaxAgentAge = 60, 100
female = 0
male = 1
fertility = [(12, 15, 40, 50),
             (12, 15, 50, 60),
             (12, 15, 30, 40), 
             (12, 15, 40, 50)]
childbearing = fertility[0], fertility[1]   # female , male
tagsLength = 5 # must be odd
tags0 = 0
tags1 = 2**tagsLength - 1
combatAlpha = 2

''' settings for Evolution from random distribution
agentColorScheme = 0        
distributions = [(400, None, (0, 50, 0, 50))] 
ruleGrow = True
ruleSeasons = False
ruleMoveEat = True
ruleCombat = False
ruleLimitedLife = False
ruleReplacement = False
ruleProcreate = False
ruleTransmit = False'''

''' settings for Emergent waves migration
agentColorScheme = 0        
distributions = [(300, None, (0, 20, 30, 50))]
ruleGrow = True
ruleSeasons = False
ruleMoveEat = True
ruleCombat = False
ruleLimitedLife = False
ruleReplacement = False
ruleProcreate = False
ruleTransmit = False'''

''' settings for Seasonal migration
agentColorScheme = 0        
distributions = [(400, None, (0, 50, 0, 50))] 
ruleGrow = True
ruleSeasons = True
ruleMoveEat = True
ruleCombat = False
ruleLimitedLife = False
ruleReplacement = False
ruleProcreate = False
ruleTransmit = False'''

''' settings for societal evolution
agentColorScheme = 3       
distributions = [(300, None, (0, 50, 0, 50))] 
ruleGrow = True
ruleSeasons = False
ruleMoveEat = True
ruleCombat = False
ruleLimitedLife = True
ruleReplacement = False
ruleProcreate = True
ruleTransmit = False'''

# settings for cultural transmission
agentColorScheme = 4
#distributions = [(300, None, (0, 50, 0, 50))] 
distributions = [(200, tags0, (0, 50, 0, 50)), (200, tags1, (0, 50, 0, 50))]
ruleGrow = True
ruleSeasons = False
ruleMoveEat = True
ruleCombat = False
ruleLimitedLife = False
ruleReplacement = False
ruleProcreate = False
ruleTransmit = True


#distributions = [(200, tags0, (0, 20, 30, 50)), (200, tags1, (30, 50, 0, 20))]

''' 
Global functions
'''

def initAgent(agent, tags, distribution):
    newLocation = agent.getEnv().getRandomFreeLocation(distribution)
    if newLocation == None:
        return False
    agent.setLocation(newLocation)
    agent.setMetabolism(random.randint(1, maxAgentMetabolism))
    agent.setVision(random.randint(1, maxAgentVision))
    agent.setInitialEndowment(random.randint(initEndowment[0], initEndowment[1]))
    agent.setAge(random.randint(minmaxAgentAge[0], minmaxAgentAge[1]))
    sexe = random.randint(0,1)
    agent.setSexe(sexe)
    agent.setFertility((random.randint(childbearing[sexe][0],childbearing[sexe][1]), random.randint(childbearing[sexe][2],childbearing[sexe][3])))
    if tags == None:
        tags = random.getrandbits(tagsLength)
    agent.setTags((tags, tagsLength))
    return True
    
''' 
View Class
'''
class View: 
    
    # this gets called first
    def __init__(self, screenSize, env, agents):
        # init view
        pygame.init()
        pygame.display.set_caption("Sugarscape")
        self.screenSize = screenSize
        self.screen = pygame.display.set_mode(screenSize)
        self.quit = False
        self.siteSize = screenSize[0] / env.gridWidth
        self.radius = int(self.siteSize * 0.5)
        # init env
        self.env = env
        self.season = ""
        # init agents population
        self.agents = agents
        self.population = [len(self.agents)]
        self.metabolismMean = []
        self.visionMean = []
        # init time
        self.iteration = 0
        self.clock = pygame.time.Clock()

    # display agent switch case (dictionary)
    def all(self, agent):
        return colorRed

    def bySexe(self, agent):
        if agent.getSexe() == female:
            return colorPink
        else:
            return colorBlue
    
    def byMetabolism(self, agent):
        if agent.getMetabolism() > 2:
            return colorRed
        else:
            return colorBlue
    
    def byVision(self, agent):
        if agent.getVision() > 3:
            return colorRed
        else:
            return colorBlue

    def byGroup(self, agent):
#        if bin(agent.getTags()).count('1') > agent.getTagsLength()>>1:
        if agent.getTribe() == 1:
            return colorRed
        else:
            return colorBlue

    agentColorSchemes = {0:all, 1:bySexe, 2:byMetabolism, 3:byVision, 4:byGroup}
    
    # remove or replace agent
    def findDistribution(self, tags):
        getTribe = lambda x, y: round(float(bin(x).count('1')) / float(y))
        tribe = getTribe(tags, tagsLength)
        for (n, t, d) in distributions:
            if t != None and getTribe(t, tagsLength) == tribe:
                # found a distribution for tags
                return d
        else:
            # or return best guess
            return d

    # replace or remove agent
    def removeAgent(self, agent):
        if ruleReplacement:
            # replace with agent of same tribe
            tags = agent.getTags()
            if initAgent(agent, tags, self.findDistribution(tags)):
                self.env.setAgent(agent.getLocation(), agent)
            else:
                print "initAgent failed!"
                self.agents.remove(agent)
        else:
            self.agents.remove(agent)
    
    # put game update code here
    def update(self):
        # for agents' logs
        metabolism = 0 
        vision = 0 
        
        # execute agents randomly
        random.shuffle(self.agents)
        
        # run agents' rules
        for agent in self.agents:
            # MOVE
            if ruleMoveEat:
                agent.move()
                # remove agent if he's dead
                if agent.getSugar() == 0:
                    # free environment
                    self.env.setAgent(agent.getLocation(), None)
                    # remove or replace agent
                    self.removeAgent(agent)
                    continue
                
            # COMBAT
            if ruleCombat:
                killed = agent.combat(combatAlpha)
                # if an agent has been killed, remove it
                if killed:
                    # do not free the environment, someone else is already here
                    self.removeAgent(killed)
                # remove agent if he's dead
                if agent.getSugar() == 0:
                    # free environment
                    self.env.setAgent(agent.getLocation(), None)
                    # remove or replace agent
                    self.removeAgent(agent)
                    continue
            
            # PROCREATE
            if ruleProcreate and agent.isFertile():
                mateItr = agent.mate()
                while True:
                    try:
                        # if a new baby is born, append it to the agents' list
                        self.agents.append(mateItr.next())
                    except StopIteration:
                        break
            
            # TRANSMIT
            if ruleTransmit:
                agent.transmit()
            
            # Log agent's parameters
            metabolism += agent.getMetabolism()
            vision += agent.getVision()

            # DIE
            # increment age
            if ruleLimitedLife and not agent.incAge():
                # free environment
                self.env.setAgent(agent.getLocation(), None)
                # remove or replace agent
                self.removeAgent(agent)

        # Log population
        numAgents = len(self.agents)
        self.population.append(numAgents)
        
        # Calculate and log agents' metabolism and vision mean values
        if numAgents > 0:
            self.metabolismMean.append(metabolism/float(numAgents))
            self.visionMean.append(vision/float(numAgents))

        # run environment's rules
        if ruleSeasons:
            S = (self.iteration % (2 * seasonPeriod)) / seasonPeriod
            if S < 1:
                # Summer
                self.season = "(summer, winter)"
                if ruleGrow:
                    self.env.growRegion(northRegion,growFactor1)
                    self.env.growRegion(southRegion,growFactor2)
            else:
                # winter
                self.season = "(winter, summer)"
                if ruleGrow:
                    self.env.growRegion(northRegion,growFactor2)
                    self.env.growRegion(southRegion,growFactor1)
        elif ruleGrow:
            self.season = "NA"
            self.env.grow(growFactor)

    # put drawing code here
    def draw(self):
        self.screen.fill(colorBackground)

        # display sugarscape
        for i, j in product(range(env.gridHeight), range(env.gridWidth)):
            x = i * self.siteSize
            y = j * self.siteSize
            # display sugar's capacity
            capacity = env.getCapacity((i,j))
            if capacity > 0:
                pygame.draw.rect(self.screen, colorSugar[capacity - 1], (x, y, self.siteSize - 1, self.siteSize - 1))

            # Draw agent if any
            agent = env.getAgent((i, j))
            if agent:
                pygame.draw.circle(self.screen,
                                    # select color scheme
                                    self.agentColorSchemes.get(agentColorScheme)(self, agent), 
                                    (x + self.radius, y + self.radius), 
                                    self.radius - 1)

        pygame.display.flip()

    # the main game loop
    def mainLoop(self):
        dt = 0
        framecount = 0
        framerate = 0
        update = False
        while not self.quit:
            t0 = pygame.time.get_ticks()
            # handle events
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.quit = True
                    
                elif event.type == KEYDOWN:
                    
                    if event.key == K_F1:
                        # Display agents' population widget
                        widget = WdgPopulation(self.population, "Population time series", 1000, 300)
                        widget.execute()
                        
                    elif event.key == K_F2:
                        # Display agents' wealth widget 
                        widget = WdgWealth(self.agents, "Wealth histogram", 500, 500)
                        widget.execute()

                    elif event.key == K_F3:
                        # Display agents' wealth widget 
                        widget = WdgAgent(self.metabolismMean, self.visionMean, "Agents' metabolism and vision mean values", 1000, 300)
                        widget.execute()

                    elif event.key == K_F12:
                        update = not update

            # update sugarscape
            if update:
                self.update()
                self.iteration += 1
            
            # display sugarscape state
            self.draw()

            # wait simulation step
            self.clock.tick(fps)

            # calculate and display the framerate
            t1 = pygame.time.get_ticks()
            dt += t1 - t0
            framecount += 1
            if dt >= 1000:
                dt -= 1000
                framerate = framecount
                framecount = 0
                
            # display infos
            if update:
                print "Iteration = ", self.iteration, "; fps = ", framerate, "; Seasons (N,S) = ", self.season, "; Population = ", len(self.agents), " -  press F12 to pause."

''' 
Main 
'''

if __name__ == '__main__' :
    
    env = Environment(gridSize)
    
    # add radial food site 
    env.addFoodSite(northSite, maxCapacity)
    
    # add radial food site 
    env.addFoodSite(southSite, maxCapacity)

    # grow to max capacity
    if ruleGrow:
        env.grow(maxCapacity)

    # create a lit of agents and place them in env
    agents = []
    for (numAgents, tags, distribution) in distributions:
        for i in range(numAgents):
            agent = Agent(env)
            if initAgent(agent, tags, distribution):
                env.setAgent(agent.getLocation(), agent)
                agents.append(agent)
    
    # Create a view with an env and a list of agents in env
    view = View(screenSize, env, agents)
    
    # iterate
    view.mainLoop()

