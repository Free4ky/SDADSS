from matplotlib import cm
import matplotlib.pyplot as plt
import matplotlib as mpl
from bee import Bee
from utils import *
from matplotlib.animation import FuncAnimation
from ACO.src.visualizer import visualize

mpl.use('Qt5Agg')


class Beehive:
    def __init__(self, dimension, minval, maxval):
        self.min_values = np.array([minval] * dimension)
        self.max_values = np.array([maxval] * dimension)
        self.domain, self.coords = self.get_domain()
        #self.fig = plt.figure()
        #self.ax = self.fig.gca(projection='3d')

    def get_domain(self, num_points=256):
        params = []
        for i in range(len(self.min_values)):
            params.append(np.linspace(self.min_values[i], self.max_values[i], num_points))

        domain = np.meshgrid(*params)
        return domain, list(zip(*(x.flat for x in domain)))

    @staticmethod
    def resolve_intersection(bees: list, rad):
        for i in range(len(bees) - 1):
            for j in range(i + 1, len(bees)):
                if bees[i].intersects(bees[j], rad=rad):
                    if bees[i].value < bees[j].value:
                        bees[j].go_to(bees[i].coord)
                    else:
                        bees[i].go_to(bees[j].coord)

    def calc_interval(self, bee, delta):
        return [(i - delta, i + delta) for i in bee.coord]

    def send_bees(self, bees: list, delta, num_to_send, func):
        sent_bees = []
        for bee in bees:
            ranges = self.calc_interval(bee, delta)
            for i in range(num_to_send):
                coords = tuple(map(lambda x: random.uniform(x[0], x[1]), ranges))
                sent_bees.append(Bee(coords, func))
        return sent_bees

    def optimize(self, func, num_scout: int, rad, delta, num_best, num_promising, iterations=100):
        scout_bees = sorted([Bee(random.choice(self.coords), func) for _ in range(num_scout)],
                            key=lambda bee: bee.value)
        n = int(num_scout * 0.2)
        m = int(num_scout * 0.5)
        best_bees = scout_bees[:n]
        promising_bees = scout_bees[n:m]
        Beehive.resolve_intersection(best_bees, rad=rad)
        Beehive.resolve_intersection(promising_bees, rad=rad)

        for i in range(iterations):
            #self.ax.cla()
            sent_to_best_bees = self.send_bees(best_bees, delta, num_best, func)
            sent_to_promising_bees = self.send_bees(promising_bees, delta, num_promising, func)
            all_sent_bees = sorted(sent_to_best_bees + sent_to_promising_bees, key=lambda bee: bee.value)
            #print(len(all_sent_bees))
            #points = zip(*[bee.position for bee in all_sent_bees])
            #self.ax.scatter(*points)
            #print(f'iteration: {i}')
            n = num_best
            m = num_promising
            best_bees = all_sent_bees[:n]
            promising_bees = all_sent_bees[n:m]
            # Beehive.resolve_intersection(best_bees, rad=rad)
            # Beehive.resolve_intersection(promising_bees, rad=rad)
        return all_sent_bees


if __name__ == '__main__':
    b = Beehive(2, -4, 4)
    # ani = FuncAnimation(plt.gcf(), lambda x: b.optimize(func=rastrigin,
    #                                                     num_scout=10,
    #                                                     rad=0.5,
    #                                                     delta=1,
    #                                                     num_best=20,
    #                                                     num_promising=50,
    #                                                     iterations=50))
    # plt.tight_layout()
    # plt.show()
    func = rastrigin
    bees = b.optimize(func=func,
                      num_scout=100,
                      rad=0.5,
                      delta=1,
                      num_best=20,
                      num_promising=50,
                      iterations=50)
    # for bee in x:
    #     print(f'{bee.coord}: {bee.value}')
    visualize(func, b.domain, points=[bees[0].coord], preview=False)
