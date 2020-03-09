import sys
sys.path.insert(0, '/home/efcastillo/ryu/ryu/app/intelligentProbing/tools/')
from bytes_to import *
import matplotlib.pyplot as plt
from os import scandir, getcwd
import os.path as path
import numpy as np
import numpy
import csv
from matplotlib import pyplot

#current position getcwd()
x = []
load_rx = []
cpu = []
frequency = []
reward = []

currentPath = getcwd()
print(currentPath)
csv_file = currentPath + '/states_reward_3.csv'
csv_plot = currentPath + '/reward.png'

if not path.exists(csv_file):
        print("The file does not exist")
        sys.exit()

with open(csv_file,'r') as csvfile:
    plots = csv.DictReader(csvfile)
    for row in plots:
        x.append(int(row["row"]))
        load_rx.append(Bytes_to(int(row["load_rx"])))
        cpu.append(float(row["cpu"]))
        frequency.append(float(row["frequency"]))
        reward.append(float(row["reward"]))

x = frequency
y = reward

bins = numpy.linspace(0, 600, 100)

pyplot.hist(x, bins, alpha=0.5, label='x')
pyplot.hist(y, bins, alpha=0.5, label='y')
pyplot.legend(loc='upper right')
pyplot.show()