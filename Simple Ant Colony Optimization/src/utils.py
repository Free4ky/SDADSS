import math
import random
import numpy as np
from itertools import product


def rastrigin(X: tuple, A=10):
    return A + sum([(x ** 2 - A * np.cos(2 * math.pi * x)) for x in X])


def X2(X: tuple):
    return sum(x ** 2 for x in X)


def batch_sample(l: list, sample_size: int = 32) -> list:
    return [l[i] for i in random.sample(range(len(l)), sample_size)]


def split_2d(array, splits):
    x, y = splits
    temp = np.array(np.split(np.concatenate(np.split(array, y, axis=1)), x * y))
    return temp.reshape(-1, int(temp.shape[0] ** 0.5), *temp.shape[1:])


def split_mesh(mesh_grid, splits: tuple = (8, 8)):
    meshes = []
    for i in mesh_grid:
        meshes.append(split_2d(i, splits))
    return meshes


def neighbours(cell, size):
    for c in product(*(range(n - 1, n + 2) for n in cell)):
        if c != cell and all(0 <= n < size for n in c):
            yield c
