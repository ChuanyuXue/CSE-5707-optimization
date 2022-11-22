import os
from os import listdir
import time

PATH = "../data/customized_dataset/"
# PATH = "../data/low-dimensional/"
# PATH = "../data/large_scale/"
for file in listdir(PATH):
    print(" ------------ %s -----------" % file)
    os.system("python3 GA.py -i %s" % (PATH+file))
    # os.system("python3 hillclimb.py -i %s" % (PATH+file))
