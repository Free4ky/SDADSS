from matplotlib import cm
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.use('Qt5Agg')


def visualize(func, domain, **kwargs):
    points = kwargs.get('points', None)
    X, Y = domain
    Z = func(domain)
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    #ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.plasma, linewidth=0, antialiased=False)
    if points is not None:
        x, y = zip(*points)
        z = list(map(func, points))
        ax.scatter(x, y, z)
    plt.show()
