from utils import *
from visualizer import visualize


class Ant:
    def __init__(self, coord: tuple, chunk: tuple):
        self.coord = coord
        self.chunk = chunk

    def move(self, graph, chunk_coord_map, pheromones, func, Q=1, a=1, b=1):
        possible_chunks = graph.get(self.chunk)  # array of possible transitions
        possible_coords = []
        current_pheromones = []
        weights = []
        for chunk in possible_chunks:
            c = chunk_coord_map[chunk]
            possible_coords.append(c)
            current_pheromones.append(pheromones[chunk])
            weights.append(abs((func(self.coord) - func(c)) ** -1))

        assert len(current_pheromones) == len(possible_coords) == len(weights)

        denominator = sum(map(lambda x, y: x * y,
                              map(lambda t: t ** a, current_pheromones),
                              map(lambda n: n ** b, weights)))
        P = np.array([t * f / denominator for t, f in zip(current_pheromones, weights)])
        m = np.argmax(P)
        self.chunk = possible_chunks[m]
        pheromones[self.chunk] += Q / weights[m]
        self.coord = chunk_coord_map[self.chunk]


def build_graph(mesh: tuple):
    mesh_x, mesh_y = mesh
    graph = {}
    for i in range(mesh_x.shape[0]):
        for j in range(mesh_x[0].shape[1]):
            graph[(i, j)] = list(neighbours((i, j), size=mesh_x.shape[0]))
    return graph


def get_map(ants):
    return dict([(a.chunk, a.coord) for a in ants])


class ACO:
    def __init__(self, dimension=2, minval=-4, maxval=4):
        self.ants = None
        self.min_values = np.array([minval] * dimension)
        self.max_values = np.array([maxval] * dimension)
        self.domain, self.coords = self.get_domain()
        self.splits = split_mesh(self.domain)
        self.graph = build_graph(self.splits)  # edges between areas
        self.pheromones = dict(zip(self.graph.keys(), [1e-4] * len(self.graph)))
        self.ants = self.init_ants(self.splits)

    def get_domain(self, num_points=256):
        params = []
        for i in range(len(self.min_values)):
            params.append(np.linspace(self.min_values[i], self.max_values[i], num_points))

        domain = np.meshgrid(*params)
        return domain, list(zip(*(x.flat for x in domain)))

    def init_ants(self, mesh: tuple):
        mesh_x, mesh_y = mesh
        ants = []
        for i in range(mesh_x.shape[0]):
            for j in range(mesh_y.shape[1]):
                mesh_x_ij, mesh_y_ij = mesh_x[i][j], mesh_y[i][j]
                k = mesh_x_ij.shape[0] // 2
                x, y = mesh_x_ij[k][k], mesh_y_ij[k][k]
                ants.append(Ant((x, y), (i, j)))
        return ants

    def find_ants(self, chunk):
        return [ant for ant in self.ants if ant.chunk == chunk]

    # recursive optimization function
    def optimize(self, func, current_chunk, chunk_number=None, level=0):
        if len(current_chunk[0]) == 1:  # chunk became a single point
            return
        splits = split_mesh(current_chunk)
        graph = build_graph(splits)
        pheromones = dict(zip(graph.keys(), [1e-4] * len(graph)))
        if level == 0:
            current_ants = self.ants = self.init_ants(splits)
        else:
            current_ants = self.find_ants(chunk_number)
        if len(current_ants) == 0:
            return
        chunk_cord_map = get_map(current_ants)
        for ant in current_ants:
            ant.move(graph, chunk_cord_map, pheromones, func)
        # to do: find chunks without ants, exclude them
        # to do: after splitting meshgrid into chunks coordinate defining for each of them is needed
        mesh_x, mesh_y = splits
        for i in range(mesh_x.shape[0]):
            for j in range(mesh_y.shape[0]):
                now_chunk = (mesh_x[i][j], mesh_y[i][j])
                self.optimize(func, now_chunk, chunk_number=(i, j), level=level + 1)


if __name__ == '__main__':
    a = ACO()
    func = rastrigin
    # print(a.pheromones)
    # print(list(map(lambda x: x.chunk, a.ants)))
    visualize(func, a.domain, points=list(map(lambda x: x.coord, a.ants)))
    a.optimize(func, a.domain)
    visualize(func, a.domain, points=list(map(lambda x: x.coord, a.ants)))
