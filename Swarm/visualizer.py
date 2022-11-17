from matplotlib import cm
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.use('Qt5Agg')


def vizualize(domain, domain_values, min_x, min_y, min_z):
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    X, Y = domain
    Z = domain_values

    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.plasma, linewidth=0, antialiased=False)

    ax.scatter(min_x, min_y, min_z, color='green')
    # -3.1459927713545297e-09, 3.2464235042108158e-09, -9.999999999999996
    plt.show()
