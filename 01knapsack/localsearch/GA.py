import numpy as np
import argparse
import time

#items
#[0] --> array of values
#[1] --> array of weights

def read_data(path):
    with open(path,"r") as f:
        items=[[int(k) for k in x.split(' ')] for x in f.readlines()]
        capacity = items[-1][0]
        items = np.array(items[1:-1])
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
    while fitness(idv, items, capacity) == -1:
        if p - (1 / items.shape[0]) > 0:
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

def gen_greedy_individual(items, capacity, mut, mut_type):
    ratios = [(i, item[0]/item[1]) for i,item in enumerate(items)]
    ratios.sort(key = lambda x: x[1], reverse=True)

    idv = [0 for i in range(items.shape[0])]
    total = 0
    for x in ratios:
        if total + items[x[0]][1] <= capacity:
            idv[x[0]] = 1
            total += items[x[0]][1]
    if mut > 0:
        idv = mutation(idv, mut, mut_type)
    if fitness(idv, items, capacity) == -1:
        idv = lighten(idv)
    return idv

def gen_greedy_population(N, items, capacity, mut, mut_type):
    pop = []
    pop.append(gen_greedy_individual(items, capacity, 0, mut_type))
    for i in range(N-1):
        idv = gen_greedy_individual(items, capacity, mut, mut_type)
        pop.append(idv)
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

def mutation(idv, mut, mut_type):
    # randomly selects each item with probably mut to be flipped
    if mut_type == 0:
        for i in range(len(idv)):
            if np.random.random() < mut:
                if idv[i] == 0:
                    idv[i] = 1
                else:
                    idv[i] = 0
    # picks a random number of pairs to flip values with mean equal to number of items*mut
    else:
        num_mutations = np.random.poisson(mut*items.shape[0])
        for x in range(num_mutations):
            i1 = np.random.choice(list(range(items.shape[0])))
            i2 = np.random.choice(list(range(items.shape[0])))
            temp = idv[i1]
            idv[i1] = idv[i2]
            idv[i2] = temp 
    return idv

# assuming idv is over weight, randomly flip 1s to 0s until fixed
def lighten(idv):
    while fitness(idv, items, capacity) > -1:
        num_item = sum(idv)
        drop = np.random.choice([i for i in range(items.shape[0])], p=[i/num_item for i in idv])
        idv[drop] = 0
    return idv

def new_population(N, pop, items, capacity, mut, mut_type):
    parents = selection(pop, items, capacity)
    children = []
    children.extend(parents)
    while len(children) < N:
        p1 = parents[np.random.choice(len(parents))]
        p2 = parents[np.random.choice(len(parents))]
        child = crossover(p1, p2)
        child = mutation(child, mut, mut_type)
        if fitness(child, items, capacity) == -1:
            child = lighten(child)
        children.append(child)
    return children

def GA(N, items, capacity, num_gen, p, mut, mut_type, greedy=False):
    #print('Initializing')
    if greedy:
        pop = gen_greedy_population(N, items, capacity, mut, mut_type)
    else:
        pop = gen_population(N, items, capacity, p)
    bestIdv = [0 for i in range(items.shape[0])]

    for i in range(num_gen):
        #print('POP', i)
        pop.sort(key = lambda x: fitness(x, items, capacity), reverse=True)
        if fitness(pop[0], items, capacity) > fitness(bestIdv, items, capacity):
            bestIdv = pop[0].copy() 
        pop = new_population(N, pop, items, capacity, mut, mut_type)
    
    return fitness(bestIdv, items, capacity), bestIdv


# ----------------------- Running -----------------------
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', type=str, required=True, help='Path to dataset.')
parser.add_argument('-p', '--p_val', default=0)
parser.add_argument('-m', '--mut_rate', default=0)
parser.add_argument('-t', '--mut_type', default=0)
parser.add_argument('-s', '--pop_size', default=0)
parser.add_argument('-n', '--num_gen', default=100)
parser.add_argument('-g', '--use_greedy', action='store_true')
args = parser.parse_args()

start = time.time()
items, capacity = read_data(args.input)

p = float(args.p_val)
mut = float(args.mut_rate)
mut_type = int(args.mut_type)
pop_size = int(args.pop_size)
num_gen = int(args.num_gen)
use_greedy = args.use_greedy

if not p:
    p = (capacity/(np.sum(items[:, 1])/items.shape[0])) / items.shape[0]
if not mut:
    mut = 1 / items.shape[0]
if not pop_size:
    pop_size = min(100, items.shape[0])

val, solution = GA(pop_size, items, capacity, num_gen, p, mut, mut_type, use_greedy)
print(val)
# print(solution)
print(round(time.time() - start, 3))