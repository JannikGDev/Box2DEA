from Environment import Environment
import time
import numpy as np

MUTATIONS = 10
MAX_ITERATIONS = 100
PLANK_SIZE = 2
SOLUTION_SIZE = 6*PLANK_SIZE
SELECTION_SIZE = 1
SIGMA_START = 0.2


def start():

    population = []
    best_solutions = []

    # Initialize random Population
    population.append(init_solution_decimal())

    counter = 0

    best_fitness = fitness(population[0])
    while counter < MAX_ITERATIONS:
        print("Step: " + str(counter))
        best = select_best(population, minimize=True)
        best_solutions.append(best)
        show_solution(best)
        population = [best]
        best_fitness = fitness(best)

        for i in range(0, MUTATIONS):

            sigma = SIGMA_START
            population.append(mutate_gauss_cycle_single(best, sigma))

        counter += 1

    best = population[0]
    print(best)
    print("Fitness: " + str(best_fitness))
    save_solutions(best_solutions)
    show_solution(best)


def show_solution(solution):

    env = Environment(solution, render=True)

    while env.running:
        env.step()

    return env.exit()


def init_solution_decimal():

    x = np.random.random(size=SOLUTION_SIZE)

    return x


def save_solutions(solutions):

    with open('data/best_solutions.txt', 'w') as file:  # Use file to refer to the file object

        for solution in solutions:

            line = ""

            for value in solution:
                line += str(value) + ","

            line = line[0:len(line)-1]

            file.write(line + "\n")


def select_best(population, minimize=True):

    best = population[0]
    bestFitness = fitness(best)

    for i in range(1, len(population)):

        currentFitness = fitness(population[i])

        if currentFitness <= bestFitness and minimize:
            best = population[i]
            bestFitness = currentFitness
        elif minimize == False and currentFitness >= bestFitness:
            best = population[i]
            bestFitness = currentFitness

    return best


def mutate_gauss(x, sigma):

    x_ = x.copy()

    for i in range(0, len(x_)):
        x_[i] = x_[i] + sigma * np.random.randn(1)

    x_ = np.clip(x_,0,1)

    return x_


def mutate_gauss_cycle(x, sigma):

    x_ = x.copy()

    for i in range(0, len(x_)):
        x_[i] = x_[i] + sigma * np.random.randn(1)

        if i % 2 == 0:
            if x_[i] > 1.0:
                x_[i] = x_[i] % 1.0

            if x_[i] < 0.0:
                x_[i] += 1.0

    x_ = np.clip(x_, 0, 1)

    return x_


def mutate_gauss_cycle_single(x, sigma):
    x_ = x.copy()

    selected = np.random.randint(0, len(x))

    x_[selected] = x_[selected] + sigma * np.random.randn(1)

    if selected % 2 == 0:
        if x_[selected] > 1.0:
            x_[selected] = x_[selected] % 1.0

        if x_[selected] < 0.0:
            x_[selected] += 1.0

    x_ = np.clip(x_, 0, 1)

    return x_


def fitness(solution):

    env = Environment(solution)

    while env.running:
        env.step()

    return env.exit()


if __name__ == "__main__":
    start()
