import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', type=str, required=True, help='Path to dataset.')
args = parser.parse_args()

start_time = time.time()
with open(args.input, 'r') as f:
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
t = time.time() - start_time

print(value)
print(result)    
print(t)


