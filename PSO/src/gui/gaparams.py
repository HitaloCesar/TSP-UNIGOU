from time import sleep

from pso import PSO

class GAParams:
    """Map widget states to pso properties"""
    
    def __init__(self, builder):
        """Get access to widgets and connect callbacks"""
        
        self.builder = builder
        self.progressStep = None

        self.spinPopSize = self.builder.get_object("spinNumParticles")
        self.spinGBestProbability = self.builder.get_object("spinGBestMaxP")
        self.spinPBestProbability = self.builder.get_object("spinPBestMaxP")
        self.spinNumberOfIteractions = self.builder.get_object("spinNumberOfIteractions")
        self.spinPausa = self.builder.get_object("spinPausa")
        self.adjPausa =self.builder.get_object("adjustmentPausa")
        self.checkRepair = self.builder.get_object("checkRepair")
        self.progressBar = self.builder.get_object("progressGeneration")

        self.greedyParticleEnabler = self.builder.get_object("greedyParticle")
        
        self.adjPausa.set_step_increment(0.001)
        
        self.spinNumberOfIteractions.connect('value-changed', self.maxGenChanged)
        self.maxGenChanged()
      
    def setPSO(self, pso):
        """Set the GeneticAlgorithm instance to work with"""
        assert isinstance(pso, PSO)
        self.pso = pso

    def getPopulationSize(self):
        return self.spinPopSize.get_value_as_int()
        
    def getNumberOfIteractions(self):
        """Gets the generation count defined by the user"""
        return self.spinNumberOfIteractions.get_value_as_int()

    def getGBestProbability(self):
        return self.spinGBestProbability.get_value()

    def getPBestProbability(self):
        return self.spinPBestProbability.get_value()

    def getGreedyParticleEnabled(self):
        return self.greedyParticleEnabler.get_active()
        
    def maxGenChanged(self, *widget):
        """Handles a change in the generation count limit"""
        numberOfIteractions = self.spinNumberOfIteractions.get_value_as_int()
        self.progressStep = 0.999999999 / float(numberOfIteractions)
    
    def handleEvolution(self):
        """Handles a population evolution event (progress bar)"""
        self.progressBar.set_fraction(self.pso.current_iteration * self.progressStep)
        self.progressBar.set_text("Iteration %d..." % self.pso.current_iteration)
        sleep(self.spinPausa.get_value())    