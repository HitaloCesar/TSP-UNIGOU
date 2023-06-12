from time import sleep

from pso import PSO

class GAParams:
    """Map widget states to genetic algorithm properties"""
    
    def __init__(self, builder):
        """Get access to widgets and connect callbacks"""
        
        self.builder = builder
        self.progressStep = None

        self.spinPopSize = self.builder.get_object("spinTamPopulacao")
        self.spinGBestProbability = self.builder.get_object("spinTaxaRecombinacao")
        self.spinPBestProbability = self.builder.get_object("spinTaxaMutacao")
        self.spinNumberOfIterations = self.builder.get_object("spinMaxGenerations")
        self.spinElite = self.builder.get_object("spinElite")
        self.spinTorneio = self.builder.get_object("spinTorneio")
        self.spinPausa = self.builder.get_object("spinPausa")
        self.adjTorneio = self.builder.get_object("adjustmentTorneio")
        self.adjPausa =self.builder.get_object("adjustmentPausa")
        self.radioTorneio = self.builder.get_object("radioTorneio")
        self.checkRepair = self.builder.get_object("checkRepair")
        self.progressBar = self.builder.get_object("progressGeneration")

        self.greedyParticleEnabler = self.builder.get_object("greedyParticle")
        
        self.adjPausa.set_step_increment(0.001)
        
        self.spinPopSize.connect('value-changed', self.popsizeChanged)
        self.spinNumberOfIterations.connect('value-changed', self.maxGenChanged)
        self.popsizeChanged()
        self.maxGenChanged()
      
    def setPSO(self, pso):
        """Set the GeneticAlgorithm instance to work with"""
        assert isinstance(pso, PSO)
        self.pso = pso

    def getPopulationSize(self):
        return self.spinPopSize.get_value_as_int()
        
    def getNumberOfIterations(self):
        """Gets the generation count defined by the user"""
        return self.spinNumberOfIterations.get_value_as_int()

    def getGBestProbability(self):
        return self.spinGBestProbability.get_value()

    def getPBestProbability(self):
        return self.spinPBestProbability.get_value()

    def getGreedyParticleEnabled(self):
        return self.greedyParticleEnabler.get_active()

    def writeStatus(self):
        """Adjust GeneticAlgorithm parameters based on widget values"""
        # Numeric parameters
        self.ga.popsize = self.spinPopSize.get_value_as_int()
        self.ga.pc = self.spinCrossRate.get_value()
        self.ga.pm = self.spinGBestProbability.get_value()
        self.ga.elitism = self.spinElite.get_value_as_int()
        self.ga.tournamentCount = self.spinTorneio.get_value_as_int()
        self.ga.selectionFn = self.ga.tournament
        self.ga.crossoverFn = self.ga.edgeCrossover
        self.ga.mutateFn = self.ga.swapMutate
        
    def popsizeChanged(self, *widget):
        """Handles a change in the size of the population"""
        popsize = self.spinPopSize.get_value_as_int()
        self.adjTorneio.set_upper(popsize)
        
    def maxGenChanged(self, *widget):
        """Handles a change in the generation count limit"""
        numberOfIterations = self.spinNumberOfIterations.get_value_as_int()
        self.progressStep = 0.999999999 / float(numberOfIterations)
    
    def handleEvolution(self):
        """Handles a population evolution event (progress bar)"""
        self.progressBar.set_fraction(self.pso.current_iteration * self.progressStep)
        self.progressBar.set_text("Iteration %d..." % self.pso.current_iteration)
        sleep(self.spinPausa.get_value())    