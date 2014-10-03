'''
Created on 2010-04-21

@author: rv
'''
import random
from itertools import product

class Agent:
    '''
    classdocs
    '''
    costForMatingRange = 0,0 #10,40
    tagsProbability = 0.55
    
    def __init__(self, env, x = 0, y = 0, metabolism = 4, vision = 6, endowment = 25, maxAge = 100, sexe = 0, fertility = (12,50), tags = (0, 11)):
        '''
        Constructor
        '''
        self.env = env
        self.x = x
        self.y = y
        self.metabolism = metabolism
        self.vision = vision
        self.maxAge = maxAge
        self.age = 0
        self.sexe = sexe
        self.fertility = fertility
        self.setInitialEndowment(endowment)
        self.setTags(tags)

    ''' 
    get / set section 
    '''
    def getEnv(self):
        return self.env
    
    def setLocation(self, (x, y)):
        self.x = x
        self.y = y

    def getLocation(self):
        return (self.x, self.y)
    
    def setMetabolism(self, metabolism):
        self.metabolism = metabolism
        
    def getMetabolism(self):
        return self.metabolism

    def setVision(self, vision):
        self.vision = vision
        
    def getVision(self):
        return self.vision

    def setInitialEndowment(self, endowment):
        self.endowment = endowment
        self.sugar = endowment
        if self.costForMatingRange == (0,0):
            self.costForMating = endowment
        else:
            self.costForMating = random.randint(self.costForMatingRange[0], self.costForMatingRange[1])
        
    def getSugar(self):
        return self.sugar

    def setAge(self, maxAge):
        self.maxAge = maxAge
        self.age = 0
        
    def getAge(self):
        return self.age
    
    def setSexe(self, sexe):
        self.sexe = sexe
        
    def getSexe(self):
        return self.sexe
    
    def setFertility(self, fertility):
        self.fertility = fertility
        
    def setTags(self, (tags, tagsLength)):
        self.tags = tags
        self.tagsLength = tagsLength
        self.tribe = round(float(bin(tags).count('1')) / float(tagsLength))
    
    def getTags(self):
        return self.tags

    def getTagsLength(self):
        return self.tagsLength
    
    def getTribe(self):
        return self.tribe

    ''' 
    build common lists
    '''

    # build a list of available food locations
    def getFood(self):
        food = [(x, self.y) for x in range(self.x - self.vision, self.x + self.vision + 2)
                if self.env.isLocationValid((x, self.y)) 
                and self.env.isLocationFree((x, self.y))]

        food.extend([(self.x, y) for y in range (self.y - self.vision, self.y + self.vision + 2) 
                if self.env.isLocationValid((self.x, y)) 
                and self.env.isLocationFree((self.x, y))])
        return food
    
    # build a list of possible neighbours for in neighbourhood
    def getNeighbourhood(self):
        neighbourhood = [self.env.getAgent((x,self.y)) for x in range(self.x - 1, self.x + 2)
                         if self.env.isLocationValid((x, self.y)) 
                         and not self.env.isLocationFree((x, self.y))
                         and x != self.x]
        
        neighbourhood.extend([self.env.getAgent((self.x,y)) for y in range(self.y - 1, self.y + 2)
                         if self.env.isLocationValid((self.x, y)) 
                         and not self.env.isLocationFree((self.x, y))
                         and y != self.y])
        return neighbourhood

    # build a list of possible preys around
    def getPreys(self):
        preys = [self.env.getAgent((x, self.y)) for x in range(self.x - self.vision, self.x + self.vision + 2)
                if self.env.isLocationValid((x, self.y)) 
                and not self.env.isLocationFree((x, self.y))
                and self.sugar > self.env.getAgent((x, self.y)).getSugar()
                and self.env.getAgent((x, self.y)).getTribe() != self.tribe]

        preys.extend([self.env.getAgent((self.x, y)) for y in range(self.y - self.vision, self.y + self.vision + 2)
                if self.env.isLocationValid((self.x, y)) 
                and not self.env.isLocationFree((self.x, y))
                and self.sugar > self.env.getAgent((self.x, y)).getSugar()
                and self.env.getAgent((self.x, y)).getTribe() != self.tribe])
        return preys
    
    ''' 
    rules
    '''

    # TRANSMIT
    def transmit(self):
        # build a list of possible neighbours for in neighbourhood
        neighbourhood = self.getNeighbourhood()

        # tag-flipping with neighbours
        for neighbour in neighbourhood:
            mask = 1 << random.randint(0, self.tagsLength - 1)
            neighbourTags = neighbour.getTags()
            if  (self.tags & mask) != (neighbourTags & mask):
                # flip neighbour's tag
                neighbourTags ^= mask
                # transmit new tag
                neighbour.setTags((neighbourTags, self.tagsLength))

    # AGEING
    # If age > maxAge Then the agent is dead (return False)
    def incAge(self):
        self.age += 1
        return (max(self.maxAge - self.age, 0))
    
    # FERTILITY
    # First, to have offspring, agents must be of childbearing age. 
    # Second, children born with literally no initial endowment of sugar would instantly die. 
    # We therefore require that parents give their children some initial endowment.
    # Each newborn's endowment is the sum of the (usually unequal) contributions of mother and father.
    # Dad contributes an amount equal to one half of whatever his initial endowment had been, and likewise for mom.
    # To be parents, agents must have amassed at least the amount of sugar which they were endowed at birth.
    def isFertile(self):
        return (self.age >= self.fertility[0] and self.age <= self.fertility[1] and self.sugar >= self.costForMating)

    # MATE (Generator):
    # Select a neighboring agent at random.
    # If the neighbor is fertile and of the opposite sex and at least one of the agent has an empty neighboring site, then a child is born
    # Repeat for all neighbors.
    def mate(self):
        # build a list of possible partners in neighbourhood
        neighbourhood = self.getNeighbourhood()
        
        # randomize
        random.shuffle(neighbourhood)
        
        # mate with (all) possible partners
        for neighbour in neighbourhood:
            # partner selection
            if neighbour.getSexe() == self.sexe or not neighbour.isFertile():
                continue
            # find a free location around the agent for the baby 
            freeLocation = self.findFreeLocationAround(self.x, self.y)
            if not freeLocation:
                # or find around the partner
                freeLocation = self.findFreeLocationAround(neighbour.x, neighbour.y)
            # then, give birth if a location has been found
            if freeLocation:
                yield self.createChild(neighbour, freeLocation)

    # Find a free location around x,y (for baby)
    def findFreeLocationAround(self, x, y):
        '''locations = [(i, j) for i,j in product(range(x - 1, x + 2), range(y - 1, y + 2))
                     if self.env.isLocationValid((i, j)) 
                     and self.env.isLocationFree((i, j))]'''
        locations = [(i, y) for i in range(x - 1, x + 2) if self.env.isLocationValid((i, y)) and self.env.isLocationFree((i, y))]
        locations.extend([(x, j) for j in range(y - 1, y + 2) if self.env.isLocationValid((x, j)) and self.env.isLocationFree((x, j))])
        length = len(locations)
        if length:
            return locations[random.randint(0, length - 1)]
        return None
    
    # Cross-over offspring from two parents: parent1 and parent2
    def createChild(self, parent, (x, y)):
        # cross-over parents genetics
        genitors = [self, parent]
        metabolism = genitors[random.randint(0,1)].metabolism
        vision = genitors[random.randint(0,1)].vision
        endowment = 0.5 * (genitors[0].endowment + genitors[1].endowment)
        genitors[0].sugar = max(genitors[0].sugar - 0.5 * genitors[0].endowment, 0)
        genitors[1].sugar = max(genitors[1].sugar - 0.5 * genitors[1].endowment, 0)
        ageMax = genitors[random.randint(0,1)].maxAge
        sexe = random.randint(0,1)
        fertility = genitors[random.randint(0,1)].fertility
        
        # build cultural tags from parents genetics
        mask = 1
        childTags = 0
        for tag in range(self.tagsLength):
            tag1 = self.tags & mask
            tag2 = parent.getTags() & mask
            if tag1 == tag2 or random.random() < self.tagsProbability:
                childTags |= tag1
            else:
                childTags |= tag2
            mask <<= 1
 
        # create child agent
        child = Agent(self.env, x, y, metabolism, vision, endowment, ageMax, sexe, fertility, (childTags, self.tagsLength))
        self.env.setAgent((x, y), child)
        return child

                
    # MOVE:
    # Look out as far as vision permits in the four principal lattice directions and identify the unoccupied site(s) having the most sugar.
    # If the greatest sugar value appears on multiple sites then select the nearest one.
    # Move to this site.
    # Collect all the sugar at this new position.
    # Increment the agent's accumulated sugar wealth by the sugar collected and decrement by the agent's metabolic rate.

    def move(self):
        # build a list of available food locations
        food = self.getFood()

        # randomize food locations
        random.shuffle(food)

        # find best food location
        # much faster than sorting.
        move = False
        newx = self.x
        newy = self.y
        best = self.env.getCapacity((self.x, self.y))
        minDistance = 0
        for (x,y) in food:
            capacity = self.env.getCapacity((x, y))
            distance = abs(x - self.x + y - self.y) # Manhattan distance enough due to no diagonal
            if capacity > best or (capacity == best and distance < minDistance):
                best = capacity
                minDistance = distance
                move = True
                newx = x
                newy = y

        # move to new location if any
        if move:
            self.env.setAgent((self.x, self.y), None)
            self.env.setAgent((newx, newy), self)
            self.x = newx
            self.y = newy
            
        # collect, eat and consume
        self.sugar = max(self.sugar + best - self.metabolism, 0)
        self.env.setCapacity((self.x, self.y), 0)

    '''
    # sort implementation
    def compareLocations(self, (x1, y1), (x2, y2)):
        c1 = self.env.getCapacity((x1, y1))
        c2 = self.env.getCapacity((x2, y2))
        if c1 - c2:
            # bigger is better
            return cmp(c1, c2)
        else:
            # Manhattan distance enough due to no diagonal
            d1 = abs(x1 - self.x + y1 - self.y)
            d2 = abs(x2 - self.x + y2 - self.y)
            # shorter is better
            return cmp(d2, d1)
    
    def moveSort(self):
        # build a list of available food locations
        food = getFood()
        
        # randomize food locations
        random.shuffle(food)

        if len(food):
            # add existing location (self.x, self.y) => currently not in food
            food.extend([(self.x, self.y)])
            # randomize food locations
            random.shuffle(food)
            # sort by capacity and distance
            food.sort(cmp = self.compareLocations, reverse = True)
            # move to best location
            (newx, newy) = food[0]
            self.env.setAgent((self.x, self.y), None)
            self.env.setAgent((newx, newy), self)
            self.x = newx
            self.y = newy
            # collect, eat and consume
            self.sugar = max(self.sugar + self.env.getCapacity(self.x, self.y) - self.metabolism, 0)
            self.env.setCapacity((self.x, self.y), 0)'''
        
    # COMBAT
    def combat(self, alpha):
        # build a list of available unoccupied food locations
        food = self.getFood()
        
        # build a list of potential preys
        preys = self.getPreys()
        
        # append to food safe preys (retaliation condition)
        reward = lambda cost, x : max(cost,min(cost,x))
        C0 = self.sugar - self.metabolism
        food.extend([preyA.getLocation() for preyA, preyB in product(preys, preys)
                     if preyA != preyB 
                     and preyB.getSugar() < (C0 + self.env.getCapacity(preyA.getLocation()) + reward(alpha, preyA.getSugar()))])
        
        # randomize food locations
        random.shuffle(food)

        # find best food location
        move = False
        newx = self.x
        newy = self.y
        best = self.env.getCapacity((self.x, self.y))
        minDistance = 0
        for (x,y) in food:
            capacity = self.env.getCapacity((x, y))
            agent = self.env.getAgent((x, y))
            if agent :
                capacity += reward(alpha, agent.getSugar())
            distance = abs(x - self.x + y - self.y) # Manhattan distance enough due to no diagonal
            if capacity > best or (capacity == best and distance < minDistance):
                best = capacity
                minDistance = distance
                move = True
                newx = x
                newy = y

        # move to new location if any
        killed = None
        
        if move:
            killed = self.env.getAgent((newx, newy))
            self.env.setAgent((self.x, self.y), None)
            self.env.setAgent((newx, newy), self)
            self.x = newx
            self.y = newy
            
        # kill, collect, eat and consume
        self.sugar = max(self.sugar + best - self.metabolism, 0)
        self.env.setCapacity((self.x, self.y), 0)
        
        return killed

                
