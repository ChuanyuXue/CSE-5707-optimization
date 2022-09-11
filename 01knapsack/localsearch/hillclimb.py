import numpy as np

#items
#[0] --> array of values
#[1] --> array of weights

def read_data(path):
    items = np.loadtxt(path, dtype=int)
    items = np.delete(items, 0, 0)
    return items

def obj_function(items, state, capacity):
    pass

def gen_neighbors(state):
    pass

def gen_init_state(items, capacity):
    pass

def hill_climbing(items, capacity, maxIter):
    pass


#TESTS
read_data('../data/low-dimensional/f1_l-d_kp_10_269')