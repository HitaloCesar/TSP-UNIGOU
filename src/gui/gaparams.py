from time import sleep
from geneticAlg import GeneticAlgorithm

class GAParams:
    """Map widget states to genetic algorithm properties"""
    
    def __init__(self, builder):
        """Get access to widgets and connect callbacks"""
        
        self.builder = builder
        self.progressStep = None

        self.spinPopSize = self.builder.get_object("spinTamPopulacao")
        self.spinCrossRate = self.builder.get_object("spinTaxaRecombinacao")
        self.spinMutationRate = self.builder.get_object("spinTaxaMutacao")
        self.spinMaxGenerations = self.builder.get_object("spinMaxGenerations")
        self.spinElite = self.builder.get_object("spinElite")
        self.spinTorneio = self.builder.get_object("spinTorneio")
        self.spinPausa = self.builder.get_object("spinPausa")
        self.adjElite = self.builder.get_object("adjustmentElite")
        self.adjTorneio = self.builder.get_object("adjustmentTorneio")
        self.adjPausa =self.builder.get_object("adjustmentPausa")
        self.radioTorneio = self.builder.get_object("radioTorneio")
        self.checkRepair = self.builder.get_object("checkRepair")
        self.progressBar = self.builder.get_object("progressGeneration")
        
        self.adjPausa.set_step_increment(0.001)
        
        self.spinPopSize.connect('value-changed', self.popsizeChanged)
        self.spinMaxGenerations.connect('value-changed', self.maxGenChanged)
        self.popsizeChanged()
        self.maxGenChanged()
      
    def setGA(self, ga):
        """Set the GeneticAlgorithm instance to work with"""
        assert isinstance(ga, GeneticAlgorithm)
        self.ga = ga
        
    def getMaxGenerations(self):
        """Gets the generation count defined by the user"""
        return self.spinMaxGenerations.get_value_as_int()
      
    def writeStatus(self):
        """Adjust GeneticAlgorithm parameters based on widget values"""
        # Numeric parameters
        self.ga.popsize = self.spinPopSize.get_value_as_int()
        self.ga.pc = self.spinCrossRate.get_value()
        self.ga.pm = self.spinMutationRate.get_value()
        self.ga.elitism = self.spinElite.get_value_as_int()
        self.ga.tournamentCount = self.spinTorneio.get_value_as_int()
        self.ga.selectionFn = self.ga.tournament
        self.ga.crossoverFn = self.ga.edgeCrossover
        self.ga.mutateFn = self.ga.swapMutate
        
    def popsizeChanged(self, *widget):
        """Handles a change in the size of the population"""
        popsize = self.spinPopSize.get_value_as_int()
        self.adjElite.set_upper(popsize)
        self.adjTorneio.set_upper(popsize)
        
    def maxGenChanged(self, *widget):
        """Handles a change in the generation count limit"""
        maxGenerations = self.spinMaxGenerations.get_value_as_int()
        self.progressStep = 0.999999999 / float(maxGenerations)
    
    def handleEvolution(self):
        """Handles a population evolution event (progress bar)"""
        self.progressBar.set_fraction(self.ga.currGeneration * self.progressStep)
        self.progressBar.set_text("Geração %d..." % self.ga.currGeneration)
        sleep(self.spinPausa.get_value())    