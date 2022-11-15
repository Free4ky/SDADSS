from abc import ABC, abstractmethod, ABCMeta
import math
import numpy as np
from particle import Particle
from visualizer import vizualize

"""
        swarmsize - размер роя (количество частиц)
        minvalues - список, задающий минимальные значения для каждой координаты частицы
        maxvalues - список, задающий максимальные значения для каждой координаты частицы
        currentVelocityRatio - общий масштабирующий коэффициент для скорости
        localVelocityRatio - коэффициент, задающий влияние лучшей точки,
найденной каждой частицей, на будущую скорость
        globalVelocityRatio - коэффициент, задающий влияние лучшей точки,
найденной всеми частицами, на будущую скорость
"""


class Swarm(ABC):

    def __init__(self,
                 swarmsize,
                 minvalues,
                 maxvalues,
                 currentVelocityRatio,
                 localVelocityRatio,
                 globalVelocityRatio):
        super().__init__()
        self.swarmsize = swarmsize
        assert len(minvalues) == len(maxvalues)
        assert (localVelocityRatio + globalVelocityRatio) > 4
        self.dimension = len(maxvalues)
        self.minvalues = np.array(minvalues[:])
        self.maxvalues = np.array(maxvalues[:])
        self.currentVelocityRatio = currentVelocityRatio
        self.localVelocityRatio = localVelocityRatio
        self.globalVelocityRatio = globalVelocityRatio

        self.globalBestFinalFunc = None
        self.globalBestPosition = None

        self.domain = self.get_domain()
        self.swarm = self.create_swarm()

    def __getitem__(self, item):
        return self.swarm[item]

    def create_swarm(self):
        return [Particle(self) for _ in range(self.swarmsize)]

    def get_domain(self):
        params = []
        for i in range(len(self.minvalues)):
            params.append(np.linspace(self.minvalues[i], self.maxvalues[i], 200))

        return np.meshgrid(*params)

    def nextIteration(self):
        """
        Выполнить следующую итерацию алгоритма
        """
        for particle in self.swarm:
            particle.nextIteration(self)

    @abstractmethod
    def _finalFunc(self, position: tuple, A=10):
        pass

    def getFinalFunc(self, position: tuple):
        assert len(position) == len(self.minvalues)

        finalFunc = self._finalFunc(position)

        if (self.globalBestFinalFunc == None or
                finalFunc < self.globalBestFinalFunc):
            self.globalBestFinalFunc = finalFunc
            self.globalBestPosition = position
        return finalFunc


class Swarm_Rastrigin(Swarm):
    def __init__(self,
                 swarmsize,
                 minvalues,
                 maxvalues,
                 currentVelocityRatio,
                 localVelocityRatio,
                 globalVelocityRatio):
        super(Swarm_Rastrigin, self).__init__(swarmsize,
                                              minvalues,
                                              maxvalues,
                                              currentVelocityRatio,
                                              localVelocityRatio,
                                              globalVelocityRatio)

    def _finalFunc(self, X: tuple, A=10):
        return A + sum([(x ** 2 - A * np.cos(2 * math.pi * x)) for x in X])

class Swarm_X2(Swarm):
    def __init__(self,
                 swarmsize,
                 minvalues,
                 maxvalues,
                 currentVelocityRatio,
                 localVelocityRatio,
                 globalVelocityRatio):
        super(Swarm_X2, self).__init__(swarmsize,
                                              minvalues,
                                              maxvalues,
                                              currentVelocityRatio,
                                              localVelocityRatio,
                                              globalVelocityRatio)

    def _finalFunc(self, X: tuple):
        return sum(x**2 for x in X)

if __name__ == '__main__':
    iterCount = 300

    dimension = 2
    swarmsize = 200

    minvalues = np.array([-4] * dimension)
    maxvalues = np.array([4] * dimension)
    currentVelocityRatio = 0.1
    localVelocityRatio = 1.0
    globalVelocityRatio = 5.0

    swarm = Swarm_Rastrigin(
        swarmsize,
        minvalues,
        maxvalues,
        currentVelocityRatio,
        localVelocityRatio,
        globalVelocityRatio
    )
    for n in range(iterCount):
        print("Position", swarm[0].get_position())
        print("Velocity", swarm[0].get_velocity())
        print(
            f'\nIteration {n}:\n\t Best minimum:{swarm.globalBestFinalFunc},\n\t Best position: {swarm.globalBestPosition}')

        swarm.nextIteration()

    vizualize(swarm.domain,
              swarm._finalFunc(swarm.domain),
              swarm.globalBestPosition[0], # x
              swarm.globalBestPosition[1], # y
              swarm.globalBestFinalFunc)   # z