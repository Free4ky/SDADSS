from scipy.spatial import distance

class Bee:
    def __init__(self, coord, func):
        self.func = func
        self.initialize(coord)

    def initialize(self, coord):
        self.coord = coord
        self.value = self.func(coord)
        self.position = self.get_position()

    def go_to(self, coord, list_range=None):
        if list_range is None:
            self.initialize(coord)

    def intersects(self, bee, rad):
        return distance.euclidean(self.position, bee.position) < rad


    def get_position(self):
        return *self.coord, self.value


if __name__ == '__main__':
    pass
