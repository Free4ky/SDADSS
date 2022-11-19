from matplotlib import cm
import math
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

mpl.use('Qt5Agg')


def rastrigin(*X, **kwargs):
    A = kwargs.get('A')
    return A + sum([(x ** 2 - A * np.cos(2 * math.pi * x)) for x in X])


if __name__ == '__main__':
    X = np.linspace(-4, 4, 200)
    Y = np.linspace(-4, 4, 200)

    X, Y = np.meshgrid(X, Y)

    Z = rastrigin(X, Y, A=10)
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.plasma, linewidth=0, antialiased=False)
    ax.scatter(-3.1459927713545297e-09, 3.2464235042108158e-09, -9.999999999999996)
    plt.show()
