import numpy as np
import os

for filename in os.listdir('../data/large_scale'):
    f = open('../data/large_scale/' + filename, 'r')
    lines = f.readlines()
    f.close()

    last_line = lines[-1]
    
    f = open('../data/large_scale/' + filename, 'w+')
    for line in lines[:-1]:
        f.write(line)
    f.close()

    f = open('../data/large_scale-optimum/' + filename, 'a')
    f.write('\n' + last_line)
    f.close()