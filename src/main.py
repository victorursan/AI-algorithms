from src.controller.GA import Population, GA
from src.controller.PSO import PSO
from src.models.CrossWordManager import CrossWordManager

if __name__ == '__main__':
    words = ["age", "ago", "beg", "cab", "cad", "dog"]
    print("Initial: " + str(words))
    print("PSO solution:")
    pso = PSO(words)
    print("Finished")
    for line in pso.get_best_solution():
        print(line)

    print()

    print("GA solution")
    cross_word_manager = CrossWordManager(words)
    pop = Population(CrossWordManager(words), 20, True)
    ga = GA(cross_word_manager)
    pop = ga.evolve_population_for(pop, 50)
    print("Finished")
    for line in ga.get_best_solution(pop):
        print(line)
