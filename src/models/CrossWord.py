import math
import random


class CrossWord:
    def __init__(self, cross_word_manager, words=None):
        self.__cross_word_manager = cross_word_manager
        self.__words = words
        if self.__words is None:
            self.__words = [None] * self.__cross_word_manager.number_of_words()
        self.__fitness = 0

    def __len__(self):
        return len(self.__words)

    def __getitem__(self, index):
        return self.__words[index]

    def __setitem__(self, key, value):
        self.__words[key] = value

    def __repr__(self):
        gene_string = ""
        for word in self.__words[:math.floor(self.__len__() / 2)]:
            gene_string += str(word) + "\n"
        return gene_string

    def generate_individual(self):
        for index in range(0, self.__cross_word_manager.number_of_words()):
            self.set_word(index, self.__cross_word_manager.get_word(index))
        random.shuffle(self.__words)

    def get_word(self, index):
        return self.__words[index]

    def set_word(self, index, word):
        self.__words[index] = word
        self.__fitness = 0

    def get_fitness(self):
        my_matrix = [[x for x in word] for word in self.__words[:math.floor(self.__words.__len__() / 2)]]
        for i in range(math.floor(self.__words.__len__() / 2)):
            next_word = self.__words[math.floor(self.__words.__len__() / 2) + i]
            for j in range(math.floor(self.__words.__len__() / 2)):
                if my_matrix[j][i] != next_word[j]:
                    self.__fitness += 1
        return self.__fitness

    def contains_word(self, word):
        return word in self.__words

    def get_matrix(self):
        return [[x for x in word] for word in self.__words[:math.floor(self.__words.__len__() / 2)]]