#!/usr/bin/env python
# coding: utf-8

# In[9]:


from os import listdir
from tqdm import tqdm
import time


# In[10]:


PATH = "../data/low-dimensional/"
# PATH = "../data/large_scale/"
# PATH = "/Users/chuanyu/Code/CSE-5707-optimization/01knapsack/data/customized_dataset/"


# In[11]:


def brute_force(W, wt, val, n):
    if n == 0:
        return 0
    if W >= wt[0]:
        return max(val[0] + brute_force(W - wt[0], wt[1:], val[1:], n-1), brute_force(W, wt[1:], val[1:], n-1))
    else:
        return brute_force(W, wt[1:], val[1:], n-1)


# In[12]:


values = []
time_log = []

for file in listdir(PATH):
    start_time = time.time()
    with open(PATH + file, 'r') as f:
        data = f.read().split("\n")
        data = [[int(k) for k in x.split(' ')] for x in data]
        capacity = data[-1][0]
        data = data[1:-1]
    val = [x[0] for x in data]
    wt = [x[1] for x in data]
    n = len(val)
    values.append(brute_force(capacity, wt, val, n))
    time_log.append(time.time() - start_time)


# In[13]:


# time_log = sorted(list(zip(listdir(PATH), time_log)), key=lambda x:int(x[0].split('_')[2]))
# [print("%.3f"%x) for x in [x[1] for x in sorted(time_log, key=lambda x:int(x[0].split('_')[1]))]]


# In[14]:


# result = sorted(list(zip(listdir(PATH), values)), key=lambda x:int(x[0].split('_')[2]))
# [print(x[1]) for x in sorted(result, key=lambda x:int(x[0].split('_')[1]))]
