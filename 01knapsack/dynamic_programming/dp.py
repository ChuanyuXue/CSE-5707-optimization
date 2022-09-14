#!/usr/bin/env python
# coding: utf-8

# In[28]:


from os import listdir
from tqdm import tqdm
import time


# In[29]:


PATH = "../data/large_scale/"
# PATH = "/Users/chuanyu/Code/CSE-5707-optimization/01knapsack/data/large_scale/"
# PATH = "/Users/chuanyu/Code/CSE-5707-optimization/01knapsack/data/customized_dataset/"


# In[30]:


def knapSack(W, wt, val, n):
    K = [[0 for x in range(W + 1)] for x in range(n + 1)]
  
    for i in tqdm(range(n + 1), file):
        for w in range(W + 1):
            if i == 0 or w == 0:
                K[i][w] = 0
            elif wt[i-1] <= w:
                K[i][w] = max(val[i-1] + K[i-1][w-wt[i-1]],  K[i-1][w])
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
    return K[n][w]


# In[31]:


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
    values.append(knapSack(capacity, wt, val, n))
    time_log.append(time.time() - start_time)


# In[32]:


# time_log = sorted(list(zip(listdir(PATH), time_log)), key=lambda x:int(x[0].split('_')[2]))
# [print("%.3f"%x) for x in [x[1] for x in sorted(time_log, key=lambda x:int(x[0].split('_')[1]))]]


# In[37]:


# result = sorted(list(zip(listdir(PATH), values)), key=lambda x:int(x[0].split('_')[2]))
# [print(x[1]) for x in sorted(result, key=lambda x:int(x[0].split('_')[1]))]


# In[ ]:




