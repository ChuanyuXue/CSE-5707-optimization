#!/usr/bin/env python
# coding: utf-8

# In[8]:


get_ipython().run_line_magic('load_ext', 'cython')


# In[9]:


from os import listdir
from tqdm import tqdm
import time
import numpy as np


# In[10]:


PATH = "../data/large_scale/"
# PATH = "/Users/chuanyu/Code/CSE-5707-optimization/01knapsack/data/customized_dataset/"


# In[11]:


def knapSack(W, wt, val, n):
    val = np.array(val, dtype=np.uint32)
    wt = np.array(wt, dtype=np.uint32)
    K = np.zeros(shape = (n+1, W+1), dtype=np.uint32)
    for i in tqdm(range(n + 1), file):
        for w in range(W + 1):
            if i == 0 or w == 0:
                K[i][w] = 0
            elif wt[i-1] <= w:
                K[i][w] = max(val[i-1] + K[i-1][w-wt[i-1]], K[i-1][w])
            else:
                K[i][w] = K[i-1][w]
    ## OUTPUT THE PATH      
    print('----%s Decision Result----'%file)
    
    w = W
    res = K[n][W]
    for i in range(n, 0, -1):
        if res <= 0:
            break
        if res == K[i - 1][w]:
            continue
        else:
            print(i - 1)
            res = res - val[i - 1]
            w = w - wt[i - 1]
  
    return K[n][W]


# In[12]:


# %%cython -a

# cpdef int knapSack(int[:] wt, int[:] val):
#     DEF n = 100_000
#     DEF W = 49973
#     cdef int K[n + 1][W + 1]
#     cdef int i, w
#     for i in range(n + 1):
#         for w in range(W + 1):
#             if i == 0 or w == 0:
#                 K[i][w] = 0
#             elif wt[i-1] <= w:
#                 K[i][w] = max(val[i-1] + K[i-1][w-wt[i-1]], K[i-1][w])
#             else:
#                 K[i][w] = K[i-1][w]
#     return K[n][w]


# In[ ]:


values = []
time_log = []
for file in listdir(PATH):
    start_time = time.time()
    with open(PATH + file, 'r') as f:
        data = f.read().split("\n")
        data = [[int(k) for k in x.split(' ')] for x in data[:-1]]
        capacity = data[-1][0]
        data = data[1:-1]
    val = [x[0] for x in data]
    wt = [x[1] for x in data]
    n = len(val)
    values.append(knapSack(capacity, wt, val, n))
    time_log.append(time.time() - start_time)


# In[ ]:


# time_log = sorted(list(zip(listdir(PATH), time_log)), key=lambda x:int(x[0].split('_')[2]))
# [print("%.3f"%x) for x in [x[1] for x in sorted(time_log, key=lambda x:int(x[0].split('_')[1]))]]


# In[ ]:


# result = sorted(list(zip(listdir(PATH), values)), key=lambda x:int(x[0].split('_')[2]))
# [print(x[1]) for x in sorted(result, key=lambda x:int(x[0].split('_')[1]))]

