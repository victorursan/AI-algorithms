
class Particle:
    def __init__(self, size):
        self.__data = [0] * size
        self.__fitness = 0
        self.__velocity = 0.0

    def get_data(self, index):
        return self.__data[index]

    def set_data(self, index, value):
        self.__data[index] = value

    @property
    def data(self):
        return self.__data

    @property
    def fitness(self):
        return self.__fitness

    @fitness.setter
    def fitness(self, value):
        self.__fitness = value

    @property
    def velocity(self):
        return self.__velocity

    @velocity.setter
    def velocity(self, value):
        self.__velocity = value

    def __str__(self):
        return str(self.__data)

    def __repr__(self):
        return str(self.__data)
