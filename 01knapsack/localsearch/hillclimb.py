import numpy as np
import argparse
import time

# items
# [0] --> array of values
# [1] --> array of weights


def read_data(path):
    with open(path, "r") as f:
        items = [[int(k) for k in x.split(' ')] for x in f.readlines()]
        capacity = items[-1][0]
        items = np.array(items[1:-1])
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
        init_states = [np.random.choice([0, 1], size=items.shape[0], p=[
                                        balance, 1-balance]) for i in range(10)]
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

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', type=str,
                    required=True, help='Path to dataset.')
parser.add_argument('-n', '--num_nbr', default=10)
parser.add_argument('-m', '--max_iter', default=100)
args = parser.parse_args()
num_neighbors = args.num_nbr
max_iter = args.max_iter

start = time.time()
items, capacity = read_data(args.input)

best_state, val, count = hill_climbing(
    items, capacity, num_neighbors, max_iter)
print(val)
# print(list(best_state))
print(round(time.time() - start, 3))
