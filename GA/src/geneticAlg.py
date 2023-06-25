from random import SystemRandom

from tsp import TSP

class GeneticAlgorithm(object):
    def __init__(self, problem):
        """Initializer"""
        self.r = SystemRandom()
        self.popsize = 50
        self.pc = 0.6
        self.pm = 0.01
        self.totalFitness = None
        self.population = []
        self.newPopulation = []
        self.fitness = []
        self.currGeneration = 1
        self.elitism = 0
        self.tournamentCount = 0
        self.selectionFn = self.tournament
        self.crossoverFn = self.edgeCrossover
        self.mutateFn = self.swapMutate
        self.problem = problem

        self.bestIndividualCostIter = []
        
    #==========================================================================
    #---=== Base functions ===
    #==========================================================================
    
    def randomPopulation(self):
        """Fills population with random individuals"""
        self.population.clear()
        for _ in range( self.popsize ):
            self.population.append( self.problem.randomIndividual() )
            
    def insertElite(self):
        """Fills n elements of the new population with elite"""
        if self.elitism == 0:
            return              
        strongestIdx = self.getNStrongestIdx(self.elitism)
        for i in strongestIdx:
            self.newPopulation.append(self.population[i])
    
    def evolve(self):
        """Evolves population by 1 generation"""
        self.newPopulation = []
        if not self.fitness:    #first time
            self.evaluatePopFitness()
        self.crossover()
        self.mutateFn()
        self.insertElite()
        self.currGeneration += 1
        self.population = self.newPopulation
        self.evaluatePopFitness()

        self.bestIndividualCostIter.append(1/self.bestIndividualTuple()[1])
    
    #==========================================================================
    #---=== Genetic Algorithm ===
    #========================================================================== 
           
    def crossover(self):
        """Crossover genetic operator"""
        while len(self.newPopulation) < (self.popsize - self.elitism):
            parent1Idx = self.selectIndividual()
            parent2Idx = self.selectIndividual()
            if self.r.random() <= self.pc:
                children = self.crossoverFn(parent1Idx, parent2Idx)
            else:
                children = ( self.population[parent1Idx].copy(),
                            self.population[parent2Idx].copy() )
            self.newPopulation.extend(children)
        self.newPopulation = self.newPopulation[:(self.popsize - self.elitism)]
           
    def swapMutate(self):
        """Swap mutation genetic operator"""
        for idx in range( len(self.newPopulation) ):
            for genA in range( len(self.problem.elements) ): 
                if self.r.random() < self.pm:
                    #Choose random gene index to swap
                    genB = genA
                    while genB == genA:
                        genB = self.r.choice( self.problem.elements )
                    #Swap gene
                    tmp = self.newPopulation[idx][genA]
                    self.newPopulation[idx][genA] = self.newPopulation[idx][genB]
                    self.newPopulation[idx][genB] = tmp
    
    #==========================================================================
    #---=== Population evaluation ===
    #==========================================================================

    def fitnessFunction(self, ind):  
        """Fitness function"""
        fitness = 0
        for i in range( len(ind) - 1 ):
            idx0 = ind[i]
            idx1 = ind[i + 1]
            x0,y0 = self.problem.coords[idx0]
            x1,y1 = self.problem.coords[idx1]
            fitness += (x1 - x0)**2 + (y1 - y0)**2
        return 1/fitness
        
    def evaluatePopFitness(self):
        """Evaluate fitness for all individuals"""    
        self.fitness.clear()
        for i in self.population:
            self.fitness.append( self.fitnessFunction(i) )
        self.totalFitness = sum(self.fitness)

    #==========================================================================
    #---=== Individuals retrieval ===
    #==========================================================================
    
    def getNStrongestIdx(self, count=1):
        """Gets the n strongest individuals indexes"""        
        assert count > 0
        sortedTuples = sorted(zip(self.fitness, range(self.popsize)), reverse=True)
        strongestIdx = []
        size = min( (count, len(sortedTuples)) )
        for i in range(size):
            strongestIdx.append(sortedTuples[i][1])
        return strongestIdx

    def bestIndividualTuple(self, key=0):
        """Returns a tuple with the best individual and its fitness"""
        assert key >= 0
        idx = self.getNStrongestIdx()[0]
        return (self.population[idx], 
                self.fitness[idx],
                self.currGeneration)

    #==========================================================================
    #---=== Selection methods ===
    #==========================================================================

    def tournament(self):
        """Selects an individual by tournament method"""     
        individualIdxs = []
        for _ in range(self.tournamentCount):
            i = self.r.choice(range(self.popsize))
            individualIdxs.append(i)
        currFitness = 0
        currIndex = 0
        for i in individualIdxs:
            fitness = self.fitness[i]
            if fitness > currFitness:
                currFitness = fitness
                currIndex = i
        return currIndex
            
    def selectIndividual(self):
        """Selects an individual"""
        return self.selectionFn()
    
    
    #==========================================================================
    #---=== Crossover types ===
    #==========================================================================
        
    def edgeCrossover(self, p1Idx, p2Idx):
        """Edge crossover"""
        p1 = self.population[p1Idx]
        p2 = self.population[p2Idx]
        #Creating adjacency matrices for parents
        adjP1 = {}
        adjP2 = {}
        for i in range( len(p1) ):
            idx1 = i - 1
            idx2 = i + 1 if ( i + 1 ) < ( len(p1) - 1 ) else 0
            adjP1[ p1[i] ] = ( p1[idx1], p1[idx2] )
            adjP2[ p2[i] ] = ( p2[idx1], p2[idx2] )
        #Creating global adjacency matrix
        adjUnion = {}
        for i in range( len(p1) ):
            adjUnion[ p1[i] ] = set( adjP1[ p1[i] ] + adjP2[ p1[i] ] )
        
        #Edge recombination algorithm
        k = []                        #K <-- the empty list
        n = self.r.choice((p1,p2))[0] #N <-- the fst node of a random parent.
        #Set
        setP1 = set(p1)
        while True:
            k.append(n)
            if len(k) >= len(p1):
                break
            
            #Remove N from all neighbor lists
            for i in range( len(p1) ):
                try:
                    adjUnion[ p1[i] ].remove(n)
                except KeyError:
                    pass
            
            #If N's neighbor list is non-empty
            if len( adjUnion[n] ) > 0:
                #neighbor of N with the fewest neighbors in its list 
                #(or a random one, should there be multiple)
                options = {} # length: (nodes)
                for neighbor in adjUnion[n]:
                    neighborCount = len ( adjUnion[neighbor] )
                    if neighborCount not in options.keys():
                        options[neighborCount] = []
                    options[neighborCount].append(neighbor)
                bestSet = list( options[ min(options.keys()) ] )
                n2 = self.r.choice(bestSet)
            else:
                n2 = self.r.choice( tuple( setP1 - set(k) ) ) #random node not in K 
            n = n2
        return (k,)