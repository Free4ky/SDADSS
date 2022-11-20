from utils import *
from visualizer import visualize


class Ant:
    def __init__(self, chunk: tuple, coord: tuple):
        self.coord = coord
        self.chunk = chunk

    def move(self, graph, chunk_coord_map, pheromones, func, Q=10, a=1, b=1):
        if isinstance(graph, list):
            possible_chunks = graph
        else:
            possible_chunks = graph.get(self.chunk)  # array of possible transitions
        if possible_chunks is None:
            return
        possible_coords = []
        current_pheromones = []
        weights = []
        for chunk in possible_chunks:
            c = chunk_coord_map[chunk]
            possible_coords.append(c)
            current_pheromones.append(pheromones[chunk])
            weights.append((func(self.coord) - func(c)))

        assert len(current_pheromones) == len(possible_coords) == len(weights)

        denominator = sum(map(lambda x, y: x * y,
                              map(lambda t: t ** a, current_pheromones),
                              map(lambda n: abs(n) ** b, weights)))
        P = np.array(
            [(t ** a * abs(f) ** b) / denominator if f > 0 else 0 for t, f in zip(current_pheromones, weights)])
        m = np.argmax(P)
        self.chunk = possible_chunks[m]
        pheromones[self.chunk] += Q * abs(weights[m])  # (1 - p) * pheromones[self.chunk]
        self.coord = chunk_coord_map[self.chunk]


def build_graph(mesh: tuple):
    mesh_x, mesh_y = mesh
    graph = {}
    for i in range(mesh_x.shape[0]):
        for j in range(mesh_x.shape[1]):
            graph[(i, j)] = list(neighbours((i, j), size=mesh_x.shape[0]))
    return graph


def get_map(chunk_cord):
    return dict(chunk_cord)


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

    def init_coord(self, mesh: tuple):
        mesh_x, mesh_y = mesh
        for i in range(mesh_x.shape[0]):
            for j in range(mesh_y.shape[1]):
                mesh_x_ij, mesh_y_ij = mesh_x[i][j], mesh_y[i][j]
                k = mesh_x_ij.shape[0] // 2
                x, y = mesh_x_ij[k][k], mesh_y_ij[k][k]
                yield (i, j), (x, y)

    def init_ants(self, mesh: tuple):
        coords = self.init_coord(mesh)
        temp = [Ant(*i) for i in coords for _ in range(1)]
        return temp

    def find_ants(self, chunk):
        return [ant for ant in self.ants if ant.chunk == chunk]

    def find_neighbour_ants(self, chunk, graph):
        neighbour_chunks = graph.get(chunk)
        if neighbour_chunks is None:
            return
        return [ant for ant in self.ants if ant.chunk in neighbour_chunks]

    # recursive optimization function
    def optimize(self, func, current_chunk, chunk_number=None, chunk_pheromone=1e-4, old_neighbours=None,
                 old_graph=None,
                 p=0.3,
                 level=0):
        if len(current_chunk[0]) == 1:  # chunk became a single point
            return
        size = (32, 32) if level == 0 else (2, 2)
        splits = split_mesh(current_chunk, splits=size)
        graph = build_graph(splits)
        pheromones = dict(zip(graph.keys(), [chunk_pheromone] * len(graph)))
        if level == 0:
            current_ants = self.ants = self.init_ants(splits)
            neighbour_ants = None
            visualize(func, self.domain, points=list(map(lambda x: x.coord, self.ants)), preview=True)
        else:
            current_ants = self.find_ants(chunk_number)
            neighbour_ants = self.find_neighbour_ants(chunk_number, old_graph)
        print(f'{level}: {len(current_ants)}, {graph}, shape: {splits[0].shape}')
        if len(current_ants) == 0:
            return
        chunk_cord_map = get_map(list(self.init_coord(splits)))
        possible_chunks = [(i, j) for i in range(splits[0].shape[0]) for j in range(splits[0].shape[1])]
        for ant in current_ants:
            ant.move(possible_chunks, chunk_cord_map, pheromones, func)
        if level > 1:
            # possible_chunks = [(i, j) for i in range(splits[0].shape[0]) for j in range(splits[0].shape[1])]
            for ant in old_neighbours:
                ant.move(possible_chunks, chunk_cord_map, pheromones, func)
        for k, v in pheromones.items():
            pheromones[k] *= (1 - p)
        # to do: find chunks without ants, exclude them
        # to do: after splitting meshgrid into chunks coordinate defining for each of them is needed
        mesh_x, mesh_y = splits
        for i in range(mesh_x.shape[0]):
            for j in range(mesh_y.shape[0]):
                now_chunk = (mesh_x[i][j], mesh_y[i][j])
                self.optimize(func,
                              now_chunk,
                              chunk_number=(i, j),
                              chunk_pheromone=pheromones[(i, j)],
                              old_neighbours=neighbour_ants,
                              old_graph=graph,
                              level=level + 1)


if __name__ == '__main__':
    a = ACO()
    func = rastrigin
    # print(a.pheromones)
    # print(list(map(lambda x: x.chunk, a.ants)))
    a.optimize(func, a.domain)
    print(len(a.ants))
    visualize(func, a.domain, points=list(map(lambda x: x.coord, a.ants)))
