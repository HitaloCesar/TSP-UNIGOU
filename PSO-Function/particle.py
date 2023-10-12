import numpy as np

class Particle:
    def __init__(self, pso, x=2.0, y=2.0, x_v=0.5, y_v=0.5, inertia_w=0.2, cognitive_w=0.6, social_w=0.8):
        self.pso = pso
        self.X = np.array([x,y])
        self.velocity = np.array([x_v, y_v])

        self.fitness = pso.getFunction()(*self.X)

        self.inertia_w = inertia_w
        self.cognitive_w = cognitive_w
        self.social_w = social_w

        self.particle_best_X = self.X

        self.particle_history = [np.append(self.X, self.fitness)]

    def update(self):
        r1 = np.random.rand(2)
        r2 = np.random.rand(2)
        cognitive_component = self.cognitive_w * r1 * (self.getParticleBestX() - self.X)
        social_component = self.social_w * r2 * (self.pso.getGlobalBestX() - self.X)
        self.velocity = self.inertia_w * self.velocity + cognitive_component + social_component

        self.X += self.velocity
        self.fitness = self.getParticleFitness()

        self.particle_history.append(np.append(self.X, self.fitness))

    def getParticleBestX(self):
        return self.particle_best_X

    def getParticleFitness(self):
        function_range = self.pso.getFunctionRange()
        if self.X[0] < function_range[0]:
            self.X[0] = function_range[0]
            self.velocity[0] = -self.velocity[0]
        if self.X[0] > function_range[1]:
            self.X[0] = function_range[1]
            self.velocity[0] = -self.velocity[0]
        if self.X[1] < function_range[0]:
            self.X[1] = function_range[0]
            self.velocity[1] = -self.velocity[1]
        if self.X[1] > function_range[1]:
            self.X[1] = function_range[1]
            self.velocity[1] = -self.velocity[1]

        return self.pso.getFunction()(*self.X)

    def getParticleBestFitness(self):
        return self.pso.getFunction()(*self.particle_best_X)


    def getParticleHistory(self):
        return self.particle_history