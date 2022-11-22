with open("./test.in", 'r') as f:
    data = f.read().split("\n")
    capacity = eval(data[-2])
    data = [[int(k) for k in x.split()[1:]] for x in data[:-2]]

data = data[1:]
result = []
result.append([len(data), capacity])
result = result + data

with open("./big_big_dataset", "w+") as f:
    for row in result:
        f.write("%d %d\n" % (row[0], row[1]))
