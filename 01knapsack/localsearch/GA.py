import numpy as np

#items
#[0] --> array of values
#[1] --> array of weights

def read_data(path):
    items = np.loadtxt(path, dtype=int)
    capacity = items[0][1]
    items = np.delete(items, 0, 0)
    return items, capacity

def fitness(idv, items, capacity):
    value, weight = 0, 0
    for i in range(len(idv)):
        if idv[i] == 1:
            value += items[i][0]
            weight += items[i][1]
    if weight > capacity:
        return -1
    else:
        return value

def gen_individual(items, capacity, p):
    idv = np.random.choice([0,1], size=items.shape[0], p=[1-p, p])
    while fitness(idv, items, capacity) < 0:
        p -= 1 / items.shape[0]
        idv = np.random.choice([0,1], size=items.shape[0], p=[1-p, p])
    return idv, p

def gen_population(N, items, capacity, p):
    pop = []
    p_vals = [p]
    for i in range(N):
        idv, new_p = gen_individual(items, capacity, sum(p_vals) / len(p_vals))
        pop.append(idv)
        p_vals.append(new_p)
    return pop

def selection(pop, items, capacity):
    fitness_v = [fitness(idv, items, capacity) for idv in pop]
    rel_fitness = [f / sum(fitness_v) for f in fitness_v]
    cum_probs = np.cumsum(rel_fitness)

    num_parents = int(len(pop)*0.3)
    parents = []
    for i in range(num_parents):
        luck = np.random.random()
        for idv in range(len(pop)):
            if cum_probs[idv] > luck:
                parents.append(list(pop[idv]))
                break
    return parents

def crossover(p1, p2):
    ratio = int(np.random.random()*len(p1))
    child = p1[:ratio] + p2[ratio:]
    return child

def mutation(idv, mut):
    for i in range(len(idv)):
        if np.random.random() < mut:
            if idv[i] == 0:
                idv[i] = 1
            else:
                idv[i] = 0
    return idv

def new_population(N, pop, items, capacity, mut):
    parents = selection(pop, items, capacity)
    children = []
    children.extend(parents)
    while len(children) < N:
        p1 = parents[np.random.choice(len(parents))]
        p2 = parents[np.random.choice(len(parents))]
        child = crossover(p1, p2)
        child = mutation(child, mut)
        if fitness(child, items, capacity) > -1:
            children.append(child)
    return children

def GA(N, items, capacity, num_gen, p, mut):
    print('Initializing')
    pop = gen_population(N, items, capacity, p)
    bestIdv = [0 for i in range(items.shape[0])]

    for i in range(num_gen):
        print('POP', i)
        pop.sort(key = lambda x: fitness(x, items, capacity), reverse=True)
        if fitness(pop[0], items, capacity) > fitness(bestIdv, items, capacity):
            bestIdv = pop[0].copy() 
        pop = new_population(N, pop, items, capacity, mut)
    
    return fitness(bestIdv, items, capacity), bestIdv

# ----------------------- Running -----------------------

p = 0.5 #initialization probability. lower values --> less items taken
mut = 0.1 #mutation probability. prob that a bit flips
pop_size = 20
num_gen = 100
dataset_path = '../data/low-dimensional/f1_l-d_kp_10_269'

items, capacity = read_data(dataset_path)

val, best = GA(pop_size, items, capacity, num_gen, p, mut)
print(val)
print(best)

#pop = gen_population(pop_size, items, capacity)
#print(pop[0])