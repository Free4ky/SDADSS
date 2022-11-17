import math
import random
import numpy as np


def rastrigin(X:tuple, A=10):
    return A + sum([(x ** 2 - A * np.cos(2 * math.pi * x)) for x in X])


def X2(X: tuple):
    return sum(x ** 2 for x in X)


def batch_sample(l: list, sample_size: int = 32) -> list:
    return [l[i] for i in random.sample(range(len(l)), sample_size)]


if __name__ == '__main__':
    print(X2())