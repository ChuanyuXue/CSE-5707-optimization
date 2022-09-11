import numpy as np

#items
#[0] --> array of values
#[1] --> array of weights

def read_data(path):
    items = np.loadtxt(path, dtype=int)
    capacity = items[0][1]
    items = np.delete(items, 0, 0)
    return items, capacity

def obj_function(items, state, capacity):
    value, weight = 0, 0
    state = np.array(state)
    value = np.dot(items[0], state)
    weight = np.dot(items[1], state)
    if weight > capacity:
        return -1
    else:
        return value

def gen_neighbors(state, num_neighbors):
    neighbors = []
    for i in range(min(num_neighbors, len(state))):
        new_state = np.copy(state)
        obj = np.random.randint(len(state))
        if state[obj] == 0:
            new_state[obj] = 1
            neighbors.append(new_state) 
        else:
            new_state[obj] = 0
            neighbors.append(new_state)
    return neighbors

def gen_init_state(items, capacity):
    init_state = None
    check = False
    balance = 0.2

    while not check:
        init_states = [np.random.choice([0,1], size=items.shape[0], p=[balance, 1-balance]) for i in range(10)]
        vals = [obj_function(items, state, capacity) for state in init_states]
        #print(balance, vals)
        max_val = max(vals)
        if max_val == -1:
            balance += 0.1
        else:
            init_state = init_states[vals.index(max_val)]
            check = True
    
    return init_state



def hill_climbing(items, capacity, num_neighbors, maxIter):
    best_state = gen_init_state(items, capacity)
    cur_best = obj_function(items, best_state, capacity)
    found = False

    count = 0
    while not found and count < maxIter:
        neighbors = gen_neighbors(best_state, num_neighbors)
        values = [obj_function(items, nbr, capacity) for nbr in neighbors]
        max_val = max(values)
        if max_val >= cur_best:
            cur_best = max_val
            best_state = neighbors[values.index(max_val)]
        else:
            found = True
        count += 1

    return best_state, cur_best, count


# ----------------------- Running -----------------------

# Set these parameters
num_neighbors = 10
maxIter = 100
dataset_path = '../data/large_scale/knapPI_1_10000_1000_1'

items, capacity = read_data(dataset_path)

best_state, val, count = hill_climbing(items, capacity, num_neighbors, maxIter)
print(val)
#print(list(best_state))