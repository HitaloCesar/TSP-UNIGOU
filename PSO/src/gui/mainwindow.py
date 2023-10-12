from gi.repository import Gtk
from os.path import join

from sys import exit

from pso import PSO
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
        window.set_resizable(True)
        
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        window.add(box)
        widget_from_xml = self.builder.get_object("dwgTSP")
        box.add(widget_from_xml)

        window.show_all()

    def execute(self, widget):
        """Execute Genetic Algorithm until last generation"""
        #GUI Helpers
        iteractions = self.gaparams.getNumberOfIteractions()
        popSize = self.gaparams.getPopulationSize()
        pbest = self.gaparams.getPBestProbability()
        gbest = self.gaparams.getGBestProbability()
        cities = self.problem.getCities(self.solviewer.getNumberOfCities())
        greedyParticle = self.gaparams.getGreedyParticleEnabled()
        self.pso = PSO(iteractions=iteractions, population_size=popSize, pbest_probability=pbest, gbest_probability=gbest, cities=cities, greedyParticle=greedyParticle)
        self.gaparams.setPSO(self.pso)
        self.solviewer.setPSO(self.pso)
        self.solviewer.clear()
        self.gaparams.handleEvolution()
        self.solviewer.handleEvolution()
        #Evolutions
        for t in range(0, iteractions):
            #Evolving population
            self.pso.iterate(t)
            self.gaparams.handleEvolution()
            self.solviewer.handleEvolution()
            #Updating GUI
            while Gtk.events_pending():
                Gtk.main_iteration()
        
        # Plot convergence graph in the end
        plt.figure(0)
        plt.plot(self.pso.gcost_iter, 'g')
        plt.title('Convergence Graph')
        plt.ylabel('Distance')
        plt.xlabel('Iteraction')
        plt.draw()
        plt.show()

    def run(self):
        """Run the main user interface"""
        Gtk.main()