from random import SystemRandom
from math import sqrt, pi, sin, cos

class TSP:
    def __init__(self):
        self.coords = []
        self.r = SystemRandom()
        self.setCityCount(1000)
        
    def setCityCount(self, cityCount):
        self.cityCount = cityCount
        self.elements = range(self.cityCount) 
        self.randomCities()
        
    def randomCities(self):
        self.coords.clear()
        for _ in range(self.cityCount):
            x,y = self.r.random(), self.r.random()
            self.coords.append( (x,y) )
            
    def circularCities(self):
        self.coords.clear()
        step = 2*pi / self.cityCount
        currAngle = self.r.random() * 2*pi
        for _ in range(self.cityCount):
            x = 0.5 + 0.5*cos(currAngle)
            y = 0.5 + 0.5*sin(currAngle)
            currAngle += step
            self.coords.append( (x,y) )
    
    def randomIndividual(self):
        individual = list(self.elements)
        self.r.shuffle(individual)
        return individual

    def getCities(self, n):
        return self.coords[:n]
    