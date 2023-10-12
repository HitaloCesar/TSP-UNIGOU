# -*- coding: utf-8 -*-

from math import pi
from operator import itemgetter

from pso import PSO

SHOW_LAST = 5
MSG_1ST = "<b>Best Particle</b>"
MSG_OTHERS = "<b>%d° best particle</b>"

class SolutionViewer:
    """View best solutions from the PSO
    
        bestTuples: list of tuples
            [(individual, fitness, generation) , ... ]
    """
    def __init__(self, builder, problem):
        """Initialize widget values and connect callbacks"""
        self.builder = builder
        self.shownIndiv = 0
        self.bestTuples = []
        self.problem = problem
        self.pso = None
        
        self.cities = self.builder.get_object("dwgTSP")
        self.cities.connect("draw", self.drawCities)
        self.paned = self.builder.get_object("paned1")
        self.frameParams = self.builder.get_object("frameParams")
        self.frameViewer = self.builder.get_object("frameViewer")
        self.btnPrevious = self.builder.get_object("btnPreviousSol")
        self.btnNext = self.builder.get_object("btnNextSol")
        self.btnRandomCities = self.builder.get_object("btnRandomCities")
        self.btnCircularCities = self.builder.get_object("btnCircularCities")
        self.btnPaned = self.builder.get_object("btnPaned")
        self.lblRank = self.builder.get_object("lblRank")
        self.spinCities = self.builder.get_object("spinCidades") 
        self.adjCities = self.builder.get_object("adjustmentCidades")
        
        self.btnPrevious.connect("clicked", self.previousSolution)
        self.btnNext.connect("clicked", self.nextSolution)
        self.btnRandomCities.connect("clicked", self.randomCities)
        self.btnCircularCities.connect("clicked", self.circularCities)
        self.btnPaned.connect("toggled", self.togglePaned)
        self.adjCities.connect("value-changed", self.changeCityCount)
        self.updateSensivity()
        self.changeCityCount()
        
    def setPSO(self, pso):
        """Set the PSO instance to work with"""
        assert isinstance(pso, PSO)
        self.pso = pso
        
    def clear(self):
        #Updating title labels
        self.lblRank.set_markup(MSG_1ST)
        self.bestTuples.clear()
        
    def togglePaned(self, widget):
        """Toggles sidebar visibility"""
        if self.btnPaned.get_active():
            x = self.frameParams.size_request().width
            self.paned.set_position(x)
        else:
            self.paned.set_position(0)

    def getNumberOfCities(self):
        return self.spinCities.get_value_as_int()

    def changeCityCount(self, *widget):
        """Change number of cities"""
        self.problem.setCityCount( self.spinCities.get_value_as_int() )
        self.clear()
        self.cities.queue_draw()
            
    def randomCities(self, *widget):
        """Generate random cities coordinates"""
        self.problem.randomCities()
        self.clear()
        self.cities.queue_draw()
        
    def circularCities(self, *widget):
        """Generate circular map"""
        self.problem.circularCities()
        self.clear()
        self.cities.queue_draw()

    #==========================================================================
    #---=== Best Individuals Retrieval ===
    #==========================================================================

    def handleEvolution(self):
        """Handle a population evolution event"""
        assert isinstance(self.pso, PSO)
        
        #Adding SHOW_LAST entries to the list
        particles = self.pso.getNStrongestParticles(SHOW_LAST)

        for particle in particles:
            route = particle.route
            coordRoute = [city.toCoord() for city in route]

            newEntry = (
                coordRoute,
                particle.pbest_cost,
                0
            )
            self.bestTuples.append(newEntry)
        
        #Sorting, keeping first entries and requesting a display update
        self.bestTuples.sort(key=itemgetter(1), reverse=False) #order by fitness
        self.bestTuples = self.bestTuples[:SHOW_LAST]
        self.showSolution()
        self.updateSensivity()
        
    #==========================================================================
    #---=== Cities display ===
    #==========================================================================

    def drawCities(self, widget, ctx):
        self.width = widget.get_allocated_width()
        self.height = widget.get_allocated_height()
        ctx.set_source_rgb(0, 0.4, 0)
        for (x,y) in self.problem.coords:
            ctx.arc(x * self.width, y * self.height, 3, 0.0, 2.0 * pi);
            ctx.fill()
        if self.bestTuples:
            self.drawLines(ctx)

    def drawLines(self, ctx):
        moves = self.bestTuples[self.shownIndiv][0]
        x0, y0 = moves[0]
        ctx.move_to(x0 * self.width, y0 * self.height)
        ctx.set_source_rgb(0, 0, 0.4)
        ctx.set_line_width(1)
        for i in moves[1:]:
            x,y = i
            ctx.line_to(x * self.width, y * self.height)
        ctx.stroke()
            
    def showSolution(self, *widget):
        if not self.bestTuples:
            return
        fitness = self.bestTuples[self.shownIndiv][1]
        generation = self.bestTuples[self.shownIndiv][2]
        
        #Updating title labels
        if self.shownIndiv == 0:
            self.lblRank.set_markup(MSG_1ST)
        else:
            self.lblRank.set_markup(MSG_OTHERS % (self.shownIndiv + 1))
        
        self.cities.queue_draw()

    #==========================================================================
    #---=== Pager-related ===
    #==========================================================================

    def updateSensivity(self):
        """Updates pager buttons sensivity"""
        if self.shownIndiv >= len(self.bestTuples) - 1:
            self.btnNext.set_sensitive(False)
        else:
            self.btnNext.set_sensitive(True)
        if self.shownIndiv == 0:
            self.btnPrevious.set_sensitive(False)
        else:
            self.btnPrevious.set_sensitive(True)
    
    def previousSolution(self, *widget):
        """Switches to previous solution"""
        self.shownIndiv -= 1
        self.showSolution()
        self.updateSensivity()
    
    def nextSolution(self, *widget):
        """Switches to next solution"""
        self.shownIndiv += 1
        self.showSolution()
        self.updateSensivity()