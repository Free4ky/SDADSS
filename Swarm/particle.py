import numpy as np
from random import randint
from copy import deepcopy
from utils import subtract_tuples, add_tuples


class Particle(object):
    """
    Класс, описывающий одну частицу
    """

    def __init__(self, swarm):
        """
        swarm - экземпляр класса Swarm, хранящий параметры алгоритма,
список частиц и лучшее значение роя в целом
        position - начальное положение частицы (список)
        """
        # Текущее положение частицы
        self.__currentPosition = self.__getInitPosition(swarm)

        # Лучшее положение частицы
        self.__localBestPosition = deepcopy(self.__currentPosition)

        # Лучшее значение целевой функции
        self.__localBestFinalFunc = swarm.getFinalFunc(self.__currentPosition)

        self.__velocity = self.__getInitVelocity(swarm)

    def get_position(self):
        return self.__currentPosition

    def get_velocity(self):
        return self.__velocity

    def __getInitPosition(self, swarm):
        """
        Возвращает список со случайными координатами для заданного интервала изменений
        """
        dim = swarm.dimension
        x, y = randint(0, swarm.domain[0].shape[0] - 1), randint(0, swarm.domain[0].shape[1] - 1)
        return tuple((c[x][y] for c in swarm.domain))
        # return np.random.rand(swarm.dimension) * (swarm.maxvalues - swarm.minvalues) + swarm.minvalues

    def __getInitVelocity(self, swarm):
        """
        Сгенерировать начальную случайную скорость
        """
        assert len(swarm.minvalues) == len(self.__currentPosition)
        assert len(swarm.maxvalues) == len(self.__currentPosition)

        minval = -(swarm.maxvalues - swarm.minvalues)
        maxval = (swarm.maxvalues - swarm.minvalues)

        return np.random.rand(swarm.dimension) * (maxval - minval) + minval

    def nextIteration(self, swarm):
        # Случайный вектор для коррекции скорости с учетом лучшей позиции данной частицы
        rnd_currentBestPosition = np.random.rand(swarm.dimension)

        # Случайный вектор для коррекции скорости с учетом лучшей глобальной позиции всех частиц
        rnd_globalBestPosition = np.random.rand(swarm.dimension)

        veloRatio = swarm.localVelocityRatio + swarm.globalVelocityRatio
        commonRatio = (2.0 * swarm.currentVelocityRatio /
                       (np.abs(2.0 - veloRatio - np.sqrt(veloRatio ** 2 - 4.0 * veloRatio))))

        # Посчитать новую скорость
        newVelocity_part1 = commonRatio * self.__velocity

        newVelocity_part2 = (commonRatio *
                             swarm.localVelocityRatio *
                             rnd_currentBestPosition *
                             (subtract_tuples(self.__localBestPosition, self.__currentPosition)))

        newVelocity_part3 = (commonRatio *
                             swarm.globalVelocityRatio *
                             rnd_globalBestPosition *
                             (subtract_tuples(swarm.globalBestPosition, self.__currentPosition)))

        self.__velocity = newVelocity_part1 + newVelocity_part2 + newVelocity_part3

        # Обновить позицию частицы
        self.__currentPosition = add_tuples(self.__currentPosition, tuple(self.__velocity))

        finalFunc = swarm.getFinalFunc(self.__currentPosition)
        if finalFunc < self.__localBestFinalFunc:
            self.__localBestPosition = deepcopy(self.__currentPosition)
            self.__localBestFinalFunc = finalFunc
