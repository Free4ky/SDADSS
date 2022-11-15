from functools import reduce
import numpy as np


def subtract_tuples(*args):
    return tuple(reduce(lambda i, j: np.subtract(i, j), args))


def add_tuples(*args):
    return tuple(reduce(lambda i, j: np.add(i, j), args))
