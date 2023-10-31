from gi.repository import Gtk
from os.path import join

from sys import exit

from pso import PSO
from tsp import TSP 

from gui.psoparams import PSOParams
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
        self.psoparams = PSOParams(self.builder)
        self.solviewer = SolutionViewer(self.builder, self.problem)
        
        #Showing GUI
        window.set_resizable(True)
        
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        window.add(box)
        widget_from_xml = self.builder.get_object("dwgTSP")
        box.add(widget_from_xml)

        window.show_all()

    def execute(self, widget):
        """Execute PSO until last generation"""
        #GUI Helpers
        iteractions = self.psoparams.getNumberOfIteractions()
        popSize = self.psoparams.getPopulationSize()
        pbest = self.psoparams.getPBestProbability()
        gbest = self.psoparams.getGBestProbability()
        cities = self.problem.getCities(self.solviewer.getNumberOfCities())
        greedyParticle = self.psoparams.getGreedyParticleEnabled()
        self.pso = PSO(iteractions=iteractions, population_size=popSize, pbest_probability=pbest, gbest_probability=gbest, cities=cities, greedyParticle=greedyParticle)
        self.psoparams.setPSO(self.pso)
        self.solviewer.setPSO(self.pso)
        self.solviewer.clear()
        self.psoparams.update()
        self.solviewer.update()
        # Iteractions
        for t in range(0, iteractions):
            self.pso.iterate(t)
            self.psoparams.update()
            self.solviewer.update()
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