from Environment import Environment
import time
import numpy as np

POPULATION_SIZE = 5
MAX_ITERATIONS = 10
SOLUTION_SIZE = 4
SELECTION_SIZE = 1
SIGMA_START = 1


def start():

    population = []
    sigma = SIGMA_START

    # Initialize random Population
    population.append(init_solution_decimal())

    counter = 0

    fitnessData = []
    best_fitness = fitness(population[0])
    while counter < MAX_ITERATIONS:
        print("Step: " + str(counter))
        best = select_best(population, min=False)
        show_solution(best)
        population = [best]
        best_fitness = fitness(best)

        for i in range(1, POPULATION_SIZE):
            sigma = 0.2
            population.append(mutate_gauss(best, sigma))

        fitnessData.append(best_fitness)

        counter += 1

    best = population[0]
    print(best)
    print("Fitness: " + str(best_fitness))

    show_solution(best)


def show_solution(solution):

    env = Environment(solution, render=True)

    while env.running:
        env.step()

    return env.exit()


def init_solution_decimal():

    x = np.random.random(size=SOLUTION_SIZE)

    return x


def select_best(population, min=True):

    best = population[0]
    bestFitness = fitness(best)

    for i in range(1, len(population)):

        currentFitness = fitness(population[i])

        if currentFitness <= bestFitness and min:
            best = population[i]
            bestFitness = currentFitness
        elif min == False and currentFitness >= bestFitness:
            best = population[i]
            bestFitness = currentFitness

    return best


def mutate_gauss(x, sigma):

    x_ = x.copy()

    for i in range(0, len(x_)):
        x_[i] = x_[i] + sigma * np.random.randn(1)

    x_ = np.clip(x_,0,1)

    return x_

def fitness(solution):

    env = Environment(solution)

    while env.running:
        env.step()

    return env.exit()















if __name__ == "__main__":
    start()