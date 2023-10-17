import random
import string

# Target string
TARGET = "Welcome to CS547!"
TARGET_LENGTH = len(TARGET)

# Genetic Algorithm Parameters
POPULATION_SIZE = 100
MUTATION_RATE = 0.01
MAX_GENERATIONS = 10000

# Initialize population with random strings
def initialize_population(pop_size, target_length):
    return [''.join(random.choice(string.printable) for _ in range(target_length)) for _ in range(pop_size)]

# Calculate fitness as the number of matching characters
def fitness(candidate):
    return sum(1 for i in range(TARGET_LENGTH) if candidate[i] == TARGET[i])

# Select parents for reproduction using tournament selection
def tournament_selection(population, tournament_size):
    tournament = random.sample(population, tournament_size)
    return max(tournament, key=fitness)

# Perform one-point crossover with variation
def crossover(parent1, parent2):
    split_point = random.randint(1, TARGET_LENGTH - 1)
    child = parent1[:split_point] + parent2[split_point:]
    
    # Introduce variation (flip a random character)
    if random.random() < MUTATION_RATE:
        mutation_point = random.randint(0, TARGET_LENGTH - 1)
        child = child[:mutation_point] + random.choice(string.printable) + child[mutation_point + 1:]
    
    return child

# Genetic Algorithm main loop
def genetic_algorithm():
    population = initialize_population(POPULATION_SIZE, TARGET_LENGTH)
    generation = 0

    while generation < MAX_GENERATIONS:
        generation += 1

        # Evaluate fitness of each individual
        fitness_scores = [fitness(individual) for individual in population]

        best_fit = max(fitness_scores)
        best_individual = population[fitness_scores.index(best_fit)]

        print(f"Generation {generation}: {best_individual} (Fitness: {best_fit}/{TARGET_LENGTH})")

        if best_fit == TARGET_LENGTH:
            print(f"Solution found in generation {generation}: {best_individual}")
            return

        new_population = [best_individual]  # Elitism

        for _ in range(POPULATION_SIZE - 1):
            parent1 = tournament_selection(population, tournament_size=10)
            parent2 = tournament_selection(population, tournament_size=10)
            child = crossover(parent1, parent2)
            new_population.append(child)

        population = new_population

    print("Maximum generations reached. No solution found.")

# Run the genetic algorithm
genetic_algorithm()
