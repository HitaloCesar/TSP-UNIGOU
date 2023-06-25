from gi.repository import Gtk
from os.path import join

from sys import exit

from geneticAlg import GeneticAlgorithm
from tsp import TSP 

from gui.gaparams import GAParams
from gui.solviewer import SolutionViewer

import matplotlib.pyplot as plt

DATA_PATH = join('..', 'data')

class MainWindow:
    currGeneration = 0
    
    def __init__(self):
        """Initializes GUI components"""
        
        #Problem
        self.problem = TSP()
        
        #Core GUI initializer
        self.builder = Gtk.Builder()
        self.builder.add_from_file(join(DATA_PATH, 'tsp.xml'))
        self.builder.connect_signals(self)
        window = self.builder.get_object("window1")
        window.connect("destroy", exit)
        
        #Helper GUI components
        self.gaparams = GAParams(self.builder)
        self.solviewer = SolutionViewer(self.builder, self.problem)
        
        #Showing GUI
        window.show_all()

    def execute(self, widget):
        """Execute Genetic Algorithm until last generation"""
        #GUI Helpers
        self.ga = GeneticAlgorithm(self.problem)
        self.gaparams.setGA(self.ga)
        self.solviewer.setGA(self.ga)
        self.solviewer.clear()
        self.gaparams.writeStatus()
        #Initial population      
        self.ga.randomPopulation()
        self.ga.evaluatePopFitness()
        #Displaying initial population
        self.gaparams.handleEvolution()
        self.solviewer.handleEvolution()
        #Evolutions
        for _ in range(1, self.gaparams.getMaxGenerations()):
            #Evolving population
            self.ga.evolve()
            self.gaparams.handleEvolution()
            self.solviewer.handleEvolution()
            #Updating GUI
            while Gtk.events_pending():
                Gtk.main_iteration()

        plt.figure(0)
        plt.plot(self.ga.bestIndividualCostIter, 'g')
        plt.ylabel('Distance')
        plt.xlabel('Generation')
        plt.draw()
        plt.show()
    
    def run(self):
        """Run the main user interface"""
        Gtk.main()