import math
import random

from src.models.Particle import Particle


class PSO:
    def __init__(self, words=None):
        self.__particle_count = 10
        self.__target = 0  # Number for algorithm to find.
        self.__max_velocity = 4  # Maximum velocity change allowed.  Range: 0 >= V_MAX < __words_len
        self.__max_epochs = 1000
        self.__particles = []
        self.__map = []
        self.__words_len = 0
        self.__words = []
        if words is not None:
            self.__words = words
            self.__words_len = self.__words.__len__()
        self.initialize_map()
        self.initialize_particles()

    def get_fitness(self, particle):
        fitnes = 0
        Matrix = [[x for x in self.__map[point]] for point in particle.data[:math.floor(self.__words_len / 2)]]
        for i in range(math.floor(self.__words_len / 2)):
            next_word = self.__map[particle.data[math.floor(self.__words_len / 2) + i]]
            for j in range(math.floor(self.__words_len / 2)):
                if Matrix[j][i] != next_word[j]:
                    fitnes += 1
        return fitnes

    def initialize_map(self):
        for i in range(self.__words_len):
            self.__map.append(self.__words[i])
        return

    def randomly_arrange(self, particle):
        word_first = random.randrange(0, self.__words_len)
        word_second = 0
        done = False

        while not done:
            word_second = random.randrange(0, self.__words_len)
            done = word_second != word_first

        # swap word_first and word_second.
        temp = particle.get_data(word_first)
        particle.set_data(word_first, particle.get_data(word_second))
        particle.set_data(word_second, temp)
        return

    def initialize_particles(self):
        for i in range(self.__particle_count):
            new_particle = Particle(self.__words_len)
            for j in range(self.__words_len):
                new_particle.set_data(j, j)
            self.__particles.append(new_particle)
            for j in range(10):  # just any number of times to randomize them.
                self.randomly_arrange(self.__particles[-1])
            self.__particles[-1].fitness = self.get_fitness(self.__particles[-1])
        return

    def get_velocity(self):
        # After sorting, worst will be last in list.
        worst_results = self.__particles[-1].best_postion if self.__particles[-1].best_postion != 0 else 1

        for particle in self.__particles:
            vValue = (self.__max_velocity * particle.best_postion) / worst_results
            if vValue > self.__max_velocity:
                particle.velocity = self.__max_velocity
            elif vValue < 0.0:
                particle.velocity = 0.0
            else:
                particle.velocity = vValue
        return

    def copy_from_particle(self, source, destination):
        # push destination's data points closer to source's data points.
        targetA = random.randrange(0, self.__words_len)  # source's city to __target.
        targetB = 0
        indexA = 0
        indexB = 0
        tempIndex = 0

        # targetB will be source's neighbor immediately succeeding targetA (circular).
        for i in range(self.__words_len):
            if source.get_data(i) == targetA:
                if i == self.__words_len - 1:
                    targetB = source.get_data(0)  # if end of array, take from beginning.
                else:
                    targetB = source.get_data(i + 1)
                break

        # Move targetB next to targetA by switching values.
        for j in range(self.__words_len):
            if destination.get_data(j) == targetA:
                indexA = j
            if destination.get_data(j) == targetB:
                indexB = j
        # get temp index succeeding indexA.
        if indexA == self.__words_len - 1:
            tempIndex = 0
        else:
            tempIndex = indexA + 1

        # Switch indexB value with tempIndex value.
        temp = destination.get_data(tempIndex)
        destination.set_data(tempIndex, destination.get_data(indexB))
        destination.set_data(indexB, temp)

        return

    def update_particles(self):
        # Best was previously sorted to index 0, so start from the second best.
        for particle in self.__particles[1:]:
            # The higher the velocity score, the more changes it will need.
            changes = math.floor(math.fabs(particle.velocity))
            for j in range(changes):
                if random.random() > 0.5:
                    self.randomly_arrange(particle)
                # Push it closer to it's best neighbor.
                self.copy_from_particle(self.__particles[self.__particles.index(particle) - 1], particle)
            # Update pBest value.
            particle.best_postion = self.get_fitness(particle)
        return

    def PSO_algorithm(self):
        epoch = 0
        while True:
            if epoch < self.__max_epochs:
                for particle in self.__particles:
                    particle.best_postion = self.get_fitness(particle)
                    if int(particle.best_postion) == int(self.__target):
                        return particle
                self.__particles.sort(key=lambda key: key.fitness)
                self.get_velocity()
                self.update_particles()
                # print("epoch number: " + str(epoch) + "\n")
                epoch += 1
            else:
                return
        return

    def get_best_solution(self):
        particle = self.PSO_algorithm()
        return[[x for x in self.__map[point]] for point in particle.data[:math.floor(self.__words_len / 2)]]

