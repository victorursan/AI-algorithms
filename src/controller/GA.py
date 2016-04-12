import random

from src.models.CrossWord import CrossWord


class Population:
    def __init__(self, cross_word_manager, corss_words_count, initialise):
        self.__corss_words = [None] * corss_words_count
        if initialise:
            for i in range(0, corss_words_count):
                new_crossword = CrossWord(cross_word_manager)
                new_crossword.generate_individual()
                self.save_cross_words(i, new_crossword)

    def __setitem__(self, key, value):
        self.__corss_words[key] = value

    def __getitem__(self, index):
        return self.__corss_words[index]

    def save_cross_words(self, index, tour):
        self.__corss_words[index] = tour

    def get_cross_words(self, index) -> CrossWord:
        return self.__corss_words[index]

    def get_fittest(self) -> CrossWord:
        fittest = self.__corss_words[0]
        for i in range(0, self.population_size()):
            if self.get_cross_words(i).get_fitness() <= fittest.get_fitness():
                fittest = self.__corss_words[i]
        return fittest

    def population_size(self):
        return len(self.__corss_words)


class GA:
    def __init__(self, cross_word_manage):
        self.__cross_word_manage = cross_word_manage
        self.mutationRate = 0.015
        self.tournamentSize = 9
        self.elitism = True

    def evolve_population(self, pop):
        new_population = Population(self.__cross_word_manage, pop.population_size(), False)
        elitism_offset = 0
        if self.elitism:
            new_population.save_cross_words(0, pop.get_fittest())
            elitism_offset = 1

        for i in range(elitism_offset, new_population.population_size()):
            parent1 = self.cross_word_selection(pop)
            parent2 = self.cross_word_selection(pop)
            child = self.crossover(parent1, parent2)
            new_population.save_cross_words(i, child)

        for i in range(elitism_offset, new_population.population_size()):
            self.mutate(new_population.get_cross_words(i))
        return new_population

    def crossover(self, parent1, parent2):
        child = CrossWord(self.__cross_word_manage)

        start_pos = int(random.random() * parent1.__len__())
        end_pos = int(random.random() * parent1.__len__())

        for i in range(0, child.__len__()):
            if end_pos > start_pos < i < end_pos:
                child.set_word(i, parent1.get_word(i))
            elif start_pos > end_pos:
                if not (start_pos > i > end_pos):
                    child.set_word(i, parent1.get_word(i))

        for i in range(0, parent2.__len__()):
            if not child.contains_word(parent2.get_word(i)):
                for ii in range(0, child.__len__()):
                    if child.get_word(ii) is None:
                        child.set_word(ii, parent2.get_word(i))
                        break
        return child

    def mutate(self, cross_word):
        for word_pos1 in range(0, cross_word.__len__()):
            if random.random() < self.mutationRate:
                word_pos2 = int(cross_word.__len__() * random.random())

                word1 = cross_word.get_word(word_pos1)
                word2 = cross_word.get_word(word_pos2)

                cross_word.set_word(word_pos2, word1)
                cross_word.set_word(word_pos1, word2)

    def cross_word_selection(self, pop) -> CrossWord:
        cross_word = Population(self.__cross_word_manage, self.tournamentSize, False)
        for i in range(0, self.tournamentSize):
            random_id = int(random.random() * pop.population_size())
            cross_word.save_cross_words(i, pop.get_cross_words(random_id))
        return cross_word.get_fittest()

    def evolve_population_for(self, pop, times):
        new_pop = pop
        for i in range(times):
            new_pop = self.evolve_population(new_pop)
        return new_pop

    def get_best_solution(self, population):
        return population.get_fittest().get_matrix()
