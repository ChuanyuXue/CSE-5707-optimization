#!/usr/bin/env python
# coding: utf-8

# In[41]:


from os import listdir
import time


# In[42]:


# PATH = "/Users/chuanyu/Code/CSE-5707-optimization/01knapsack/data/large_scale/"
PATH = "../data/low-dimensional/"


# In[43]:


values = []
time_log = []
for file in listdir(PATH):
    start_time = time.time()
    with open(PATH + file, 'r') as f:
        data = f.read().split("\n")
        data = [[int(k) for k in x.split(' ')] for x in data]
        capacity = data[-1][0]
        data = data[1:-1]
        
    data = sorted(data, key= lambda x:x[0]/x[1], reverse=True)
    value = 0
    weight = 0
    result = []
    for row in data:
        if weight + row[1] <= capacity:
            value += row[0]
            weight += row[1]
            result.append(1)
        else:
            result.append(0)
        result += [0] * (len(data) - len(result))
    values.append(value)
    time_log.append(time.time() - start_time)
    print(result)


# In[44]:


list(zip(listdir(PATH), time_log))


# In[45]:


list(zip(listdir(PATH), values))


# In[36]:


# time_log = sorted(list(zip(listdir(PATH), time_log)), key=lambda x:int(x[0].split('_')[4]))
# [print(x[1]) for x in [x[1] for x in sorted(time_log, key=lambda x:int(x[0].split('_')[3]))]]

# result = sorted(list(zip(listdir(PATH), values)), key=lambda x:int(x[0].split('_')[4]))
# [print(x[1]) for x in sorted(result, key=lambda x:int(x[0].split('_')[3]))]


# In[ ]:




