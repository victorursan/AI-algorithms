
class CrossWordManager:
    def __init__(self, words=None):
        self.__words = []
        if words is not None:
            self.__words = words

    def add_word(self, word):
        self.__words.append(word)

    def get_word(self, index):
        return self.__words[index]

    def number_of_words(self):
        return len(self.__words)

