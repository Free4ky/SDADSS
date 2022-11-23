import random
import numpy as np
from utils import X2, rastrigin, batch_sample
from Swarm.visualizer import vizualize


class Ant:
    def __init__(self, start_point):
        self.current_point = start_point
        self.local_solution = None
        self.current_value = None

    def set_coordinate(self, position: tuple):
        self.current_point = position

    def set_current_value(self, value):
        self.current_value = value
        if self.local_solution is None:
            self.local_solution = value
        elif value < self.local_solution:
            self.local_solution = value


class ACO:
    def __init__(self, colony_size, dimension=2, minval=-4, maxval=4):
        self.min_values = np.array([minval] * dimension)
        self.max_values = np.array([maxval] * dimension)
        print(self.min_values)
        print(self.max_values)
        self.domain, self.coords = self.get_domain()
        self.pheromone = self.init_pheromone()
        self.start_point = random.choice(self.coords)
        self.ant_colony = [Ant(self.start_point) for _ in range(colony_size)]
        self.global_solution = None
        self.global_solution_coordinate = None

    def get_domain(self, num_points=200):
        params = []
        for i in range(len(self.min_values)):
            params.append(np.linspace(self.min_values[i], self.max_values[i], num_points))

        domain = np.meshgrid(*params)
        return domain, list(zip(*(x.flat for x in domain)))

    def init_pheromone(self):
        return dict(zip(self.coords, np.random.rand(len(self.coords), 1) / 1e3))

    def optimize(self, function, Q=10, a=10, b=1, **kwargs):
        iterations = kwargs.get('iterations')
        if iterations is not None:
            stochastic = True
        else:
            stochastic = False
            iterations = 1
        for i in range(iterations):
            if not stochastic:
                batch = self.coords
                output = list(map(function, batch))
                inverse_output = list(map(lambda x: x ** -1, output))
                current_pheromone = self.pheromone.values()
            for ant in self.ant_colony:
                if stochastic:
                    batch = batch_sample(self.coords)
                    current_pheromone = [self.pheromone.get(coord) for coord in batch]
                    output = list(map(function, batch))
                    inverse_output = list(map(lambda x: x ** -1, output))
                assert len(output) == len(current_pheromone)
                denominator = sum(map(lambda x, y: x * y,
                                      map(lambda x: x ** b, inverse_output),
                                      map(lambda y: y ** a, current_pheromone)))
                # calculate probabilities
                P = np.array([t * f / denominator for t, f in zip(current_pheromone, inverse_output)])
                m = np.argmax(P)
                new_coord = batch[m]
                # assert len(new_coord) == 1
                ant.set_coordinate(new_coord)
                ant.set_current_value(output[m])
                self.update_global_solution(output[m], batch[m])
                # update pheromone
                for c, o in zip(batch, inverse_output):
                    self.pheromone[c] += Q / o
            # print(f'Iteration: {i}, global solution: {self.global_solution}')
        # for ant in self.ant_colony:
        #     if self.global_solution is None and ant.current_value is not None:
        #         self.global_solution = ant.current_value
        #         self.global_solution_coordinate = ant.current_point
        #     elif ant.current_value < self.global_solution and ant.current_value is not None:
        #         self.global_solution = ant.current_value
        #         self.global_solution_coordinate = ant.current_point

    def update_global_solution(self, value, coordinate):
        if self.global_solution is None:
            self.global_solution = value
            self.global_solution_coordinate = coordinate
        elif value < self.global_solution:
            self.global_solution = value
            self.global_solution_coordinate = coordinate


if __name__ == '__main__':
    a = ACO(40)
    # print(a.coords)
    func = rastrigin
    a.optimize(func, iterations=300)
    print(a.global_solution_coordinate, a.global_solution)
    vizualize(
        a.domain,
        func(a.domain),
        min_x=a.global_solution_coordinate[0],
        min_y=a.global_solution_coordinate[1],
        min_z=func(a.global_solution_coordinate)
    )
