import math
import random
import numpy as np
from itertools import product


def rastrigin(X: tuple, A=10):
    return A + sum([(x ** 2 - A * np.cos(2 * math.pi * x)) for x in X])


def X2(X: tuple):
    return sum(x ** 2 for x in X)


def schwefel(X: tuple):
    return sum([(-x * np.sin(np.sqrt(np.abs(x)))) for x in X])
