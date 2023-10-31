import random
import math
from FileWriter import FileWriter

class City:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance(self, city):
        return math.hypot(self.x - city.x, self.y - city.y)
    
    def toCoord(self):
        return (self.x, self.y)

class Particle:
    def __init__(self, route, cost=None):
        self.route = route
        self.pbest = route
        self.current_cost = cost if cost else self.path_cost()
        self.pbest_cost = cost if cost else self.path_cost()

    def __str__(self) -> str:
        return str(self.pbest_cost)

    def update_particle_status(self, route):
        self.route = route
        self.current_cost = self.path_cost()
        if self.current_cost < self.pbest_cost:
            self.pbest = self.route
            self.pbest_cost = self.current_cost

    def path_cost(self):
        return sum([city.distance(self.route[index - 1]) for index, city in enumerate(self.route)])

    def getStringRoute(self):
        listOfCities = []
        for city in self.route:
            listOfCities.append(city.toCoord())
        return(str(listOfCities))

class PSO:
    def __init__(self, iteractions, population_size, gbest_probability=1.0, pbest_probability=1.0, cities=None, greedyParticle=False):
        psoCities = []
        for city in cities:
            psoCities.append(City(city[0], city[1]))
        self.cities = psoCities
        self.gbest = None
        self.gcost_iter = []
        self.iteractions = iteractions
        self.population_size = population_size
        self.particles = []
        self.gbest_probability = gbest_probability
        self.pbest_probability = pbest_probability
        self.current_iteration = 0
        self.greedyParticle = greedyParticle

        solutions = self.initial_population()
        self.particles = [Particle(route=solution) for solution in solutions]
    
        self.log_file = FileWriter('../data/logs/LogsPSO.txt')
        self.log_file.clear_file()
        self.log_file.write_to_file(f'iteractions= {iteractions}\npopulation_size= {population_size}\nglobal_prob= {gbest_probability}\nparticle_prob= {pbest_probability}\ngreedy_particle={greedyParticle}')

    def generate_random_route(self):
        cities1 = [self.cities[0]]
        cities2 = random.sample(self.cities[1:], len(self.cities) - 1)
        return cities1 + cities2

    def generate_greedy_route(self):
        unvisited = self.cities[:]
        del unvisited[0]
        route = [self.cities[0]]
        while len(unvisited):
            index, nearest_city = min(enumerate(unvisited), key=lambda item: item[1].distance(route[-1]))
            route.append(nearest_city)
            del unvisited[index]
        return route

    def initial_population(self):
        random_population = [self.generate_random_route() for _ in range(self.population_size - 1)]
        if (self.greedyParticle):  
            random_population = [self.generate_random_route() for _ in range(self.population_size - 1)]
            greedy_population = [self.generate_greedy_route()]
            return [*random_population, *greedy_population]
        else: 
            random_population.append(self.generate_random_route())
            return random_population

    def iterate(self, t):
        self.current_iteration += 1
        self.gbest = min(self.particles, key=lambda p: p.pbest_cost)
        self.gcost_iter.append(self.gbest.pbest_cost)

        self.log_file.write_to_file(f'Iteration = {t}, previous best cost = {self.gbest.pbest_cost}')
        for idx, particle in enumerate(self.particles):
            self.log_file.write_to_file(f'Particle {idx}: ' + str(particle.getStringRoute() + f', particle current cost = {particle.current_cost}'))

            temp_velocity = []
            gbest = self.gbest.pbest[:]
            new_route = particle.route[:]

            for i in range(1,len(self.cities)):
                pbest_prob = random.random()*self.pbest_probability
                if new_route[i] != particle.pbest[i]:
                    information_swap = (i, particle.pbest.index(new_route[i]), pbest_prob)
                    temp_velocity.append(information_swap)

            for i in range(1,len(self.cities)):
                gbest_prob = random.random()*self.gbest_probability
                if new_route[i] != gbest[i]:
                    information_swap = (i, gbest.index(new_route[i]), gbest_prob)
                    temp_velocity.append(information_swap)

            for information_swap in temp_velocity:
                if random.random() <= information_swap[2]:
                    new_route[information_swap[0]], new_route[information_swap[1]] = new_route[information_swap[1]], new_route[information_swap[0]]

            particle.update_particle_status(new_route)

            if (t >= self.iteractions - 1):
                self.log_file.write_to_file(f'Last Iteration Particle {idx}: ' + str(particle.getStringRoute()))


    def getNStrongestParticles(self, count=1):
        """Gets the n strongest individuals indexes"""        
        assert count > 0
        particlesSorted = sorted(self.particles, key=lambda x: x.pbest_cost, reverse=False)
        strongestParticles = []
        size = min( (count, len(particlesSorted)) )
        for i in range(size):
            strongestParticles.append(particlesSorted[i])
        return strongestParticles