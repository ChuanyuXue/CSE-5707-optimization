#!/usr/bin/env python
# coding: utf-8

# In[8]:

#get_ipython().run_line_magic('load_ext', 'cython')
import cython

# In[9]:


import time
import numpy as np
import argparse


# In[10]:



# PATH = "/Users/chuanyu/Code/CSE-5707-optimization/01knapsack/data/customized_dataset/"



def knapSack(W, wt, val, n):
    val = np.array(val, dtype=np.uint32)
    wt = np.array(wt, dtype=np.uint32)
    K = np.zeros(shape = (n+1, W+1), dtype=np.uint32)
    for i in range(n + 1):
        for w in range(W + 1):
            if i == 0 or w == 0:
                K[i][w] = 0
            elif wt[i-1] <= w:
                K[i][w] = max(val[i-1] + K[i-1][w-wt[i-1]], K[i-1][w])
            else:
                K[i][w] = K[i-1][w]
    ## OUTPUT THE PATH      
    print('----%s Decision Result----')
    w = W
    res = K[n][W]
    output = [0 for i in range(n)]
    for i in range(n, 0, -1):
        if res <= 0:
            break
        if res == K[i - 1][w]:
            continue
        else:
            output[i - 1] = 1
            res = res - val[i - 1]
            w = w - wt[i - 1]
    print(output)

    return K[n][W]

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', type=str, required=True, help='Path to dataset.')
args = parser.parse_args()

start_time = time.time()
with open(args.input, 'r') as f:
    data = f.read().split("\n")
    data = [[int(k) for k in x.split(' ')] for x in data]
    capacity = data[-1][0]
    data = data[1:-1]
val = [x[0] for x in data]
wt = [x[1] for x in data]
n = len(val)
value = knapSack(capacity, wt, val, n)
t = time.time() - start_time

print(value)
print(t)