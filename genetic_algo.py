#Genrtic: Not optimal 
import random
import matplotlib.pyplot as plt
import test_case as tc

W = 0
num_classes = 0
weights = []
values = []
classes = []


POPULATION_SIZE = 6
INDIVIDUAL_SIZE = 0
population = []
fitness = [0 for i in range(POPULATION_SIZE)]

MAX_STEPS = 500
CROSSOVER_RATE = 0.85
MUTATION_RATE = 0.02
REPRODUCTION_RATE = 0.3

# 1. Generate initial population: different
def generate_initial_population():
    is_selected = [0, 1]
    initial_population = []
    while len(initial_population) != POPULATION_SIZE:
        individual = random.choices(is_selected, weights=[10,1], k = INDIVIDUAL_SIZE)
        # print(individual)
        if individual not in initial_population and is_at_least_1_item_each_class(individual):
            initial_population.append(individual)
    return initial_population

# 2. Fitness function
def cal_fitness():
    for i in range(POPULATION_SIZE):
        sum_of_weight = 0
        sum_of_value = 0
        for j in range(len(population[i])):
            sum_of_weight += population[i][j] * weights[j]
            sum_of_value += population[i][j] * values[j]

        if sum_of_weight > W:
            fitness[i] = 0
        else:
            fitness[i] = sum_of_value

# 3. Selection:
def selection():
    selected_index = random.sample(range(len(population)), k=4)
    parents = []
    parents.append(population[selected_index[0]] if fitness[selected_index[0]] > fitness[selected_index[1]] else population[selected_index[1]])
    parents.append(population[selected_index[1]] if fitness[selected_index[1]] > fitness[selected_index[2]] else population[selected_index[2]])
    return parents

# 4. Crossover
def crossover(parents):
    children = []
    if random.random() >= CROSSOVER_RATE:
        return parents
    point = len(parents[0]) // 2
    children.append(parents[0][:point] + parents[1][point:])
    children.append(parents[1][:point] + parents[0][point:])
    return children

# 5. Mutation
def mutation(children):
    for child in children:
        for i in range(len(child)):
            if random.random() < MUTATION_RATE:
                child[i] = child[i]^1
    
    return children

def is_at_least_1_item_each_class(individual):
    lst_classes = [0 for i in range(num_classes)]
    for i in range(len(individual)):
        if individual[i]:
            lst_classes[classes[i]-1] = 1

    for c in lst_classes:
        if c == 0:
            return False
    
    sum_of_weight = 0
    for i in range(INDIVIDUAL_SIZE):
        sum_of_weight += (individual[i] * weights[i])
    if(sum_of_weight > W):
        return False

    return True

# 6. Generate next generation
def generate_next_population():
    next_population = []
    while len(next_population) < len(population):
        parents = selection()
        children = []
        if random.random() >= REPRODUCTION_RATE:
            children = parents
        else:
            children = crossover(parents)
            children = mutation(children)

            for child in children:
                if len(next_population) < len(population) and is_at_least_1_item_each_class(child):
                    next_population.append(child)
                    # print('got')

    return next_population

def get_fittest_individual():
    fittest_index = 0
    for i in range(POPULATION_SIZE):
        if fitness[i] > fitness[fittest_index]:
            fittest_index = i
    
    sum_of_weight = 0
    for i in range(INDIVIDUAL_SIZE):
        sum_of_weight += (population[fittest_index][i] * weights[i])

    return (sum_of_weight, fitness[fittest_index], population[fittest_index])

def get_average():
    global fitness
    return sum(fitness) // len(fitness)

def genetic_algorithm_knapsack_problem():
    global population
    # avg_fitness = []
    # print('1')
    population = generate_initial_population()
    # print('2')
    cal_fitness()
    # avg_fitness.append(get_fittest_individual()[0])

    for i in range(MAX_STEPS):
        population = generate_next_population()
        cal_fitness()
        # avg_fitness.append(get_fittest_individual()[0])

    return get_fittest_individual()
    
    # return avg_fitness


def evaluation(algo, times):
    solutions = []
    for i in range(times):
        res = algo()
        solutions.append(res[0])
    return (list(range(times)), solutions)

def draw_graph(x, y):
    plt.plot(x, y)
    plt.xlabel('Generation')
    # frequency label
    plt.ylabel('Fitness')
    # plot title
    plt.title('Genetic Algorithm')
    
    # function to show the plot
    plt.show()

if __name__=="__main__":
    for i in range(5):
        # fin = 'input/INPUT_'+str(i)+'.txt'
        # fout= 'output/genetic_algorithm/OUTPUT_'+str(i)+'.txt'

        fin = 'large_input/INPUT_'+str(i)+'.txt'
        fout= 'large_output/genetic_algorithm/OUTPUT_'+str(i)+'.txt'

        data = tc.use_testcase(fin)
        W = data[0]
        num_classes = data[1]
        weights = data[2]
        values = data[3]
        classes = data[4]
        INDIVIDUAL_SIZE = len(weights)
        tc.time_operation(genetic_algorithm_knapsack_problem, fin, 
                        len(weights), num_classes, W, fout)