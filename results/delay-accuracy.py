# https://relopezbriega.github.io/blog/2015/06/27/probabilidad-y-estadistica-con-python/
import sys
sys.path.insert(0, '/home/efcastillo/ryu/ryu/app/intelligentProbing/tools/')
from bytes_to import *
import numpy as np
from scipy import stats # importando scipy.stats
import pandas as pd # importando pandas
import matplotlib.pyplot as plt
from matplotlib import mlab
from pathlib import Path
from os import scandir, getcwd
import os.path as path
from itertools import *
from statistics import mean, stdev, median_grouped, median_high
import csv
from scipy.stats import variation
from matplotlib.patches import Polygon

def csvRead(csv_file):
	x = []
	time_csv = []
	rtt = []
	delay = []
	delay_ms = []
	jitter = []
	time_r = []
	time_s = []
	delay_r = []
	delay_s = []

	if not path.exists(csv_file):
		print("The file does not exist")
		sys.exit()

	with open(csv_file,'r') as csvfile:
		plots = csv.DictReader(csvfile)
		i = 0
		for row in plots:
			try:
				i+=1
				x.append(i)
				rtt.append(float(row["iRTT"])*1000)
				time_csv.append(float(row["Time"]))
			except Exception as e:
				#print ('Line {i} is corrupt!'.format(i = i), " File ", Path(csv_file).name)
				pass
	time_r = time_csv[1:]
	time_s = time_csv[:-1]

	for i in range(len(time_s)):
		delay.append(time_r[i] - time_s[i])
		delay_ms.append((time_r[i] - time_s[i])*1000)

	delay_r = delay[1:]
	delay_s = delay[:-1]

	for j in range(len(delay_s)):
		jitter.append(round((delay_r[j] - delay_s[j]), 3))

	rtt_accuracy = (median_grouped(rtt) * 100)/0.68
    #ipro = 0.63

    #print("Mean: ",round(mean(jitter), 5)*1000, round(sum(jitter), 3), Path(csv_file).name)
	print(median_grouped(rtt), mean(delay_ms),median_grouped(jitter), Path(csv_file).name)
	return [abs(median_grouped(jitter)*1000), mean(delay_ms), rtt_accuracy]

currentPath = getcwd()
print(currentPath)

state_05 = csvRead(currentPath + '/pcap/delay/probing_05s-delay.csv')
state_1 = csvRead(currentPath + '/pcap/delay/probing_1s-delay.csv')
state_2 = csvRead(currentPath + '/pcap/delay/probing_2s-delay.csv')
state_3 = csvRead(currentPath + '/pcap/delay/probing_3s-delay.csv')
state_4 = csvRead(currentPath + '/pcap/delay/probing_4s-delay.csv')
state_5 = csvRead(currentPath + '/pcap/delay/probing_5s-delay.csv')
state_6 = csvRead(currentPath + '/pcap/delay/probing_6s-delay.csv')
state_7 = csvRead(currentPath + '/pcap/delay/probing_7s-delay.csv')
state_8 = csvRead(currentPath + '/pcap/delay/probing_8s-delay.csv')
state_9 = csvRead(currentPath + '/pcap/delay/probing_9s-delay.csv')
state_10 = csvRead(currentPath + '/pcap/delay/probing_10s-delay.csv')
state_11 = csvRead(currentPath + '/pcap/delay/probing_11s-delay.csv')
state_12 = csvRead(currentPath + '/pcap/delay/probing_12s-delay.csv')
state_13 = csvRead(currentPath + '/pcap/delay/probing_13s-delay.csv')
state_14 = csvRead(currentPath + '/pcap/delay/probing_14s-delay.csv')
state_15 = csvRead(currentPath + '/pcap/delay/probing_15s-delay.csv')

#datos_graf = [datos_1, datos_2, datos_3, datos_4]
delay_list = [state_1[1], state_2[1], state_3[1], state_4[1], state_5[1], 
                state_6[1], state_7[1],state_8[1],state_9[1],state_10[1],state_11[1],
                state_12[1],state_13[1],state_14[1],state_15[1]]

datos_graf = [state_1[0], state_2[0], state_3[0], state_4[0], state_5[0], 
                state_6[0], state_7[0],state_8[0],state_9[0],state_10[0],state_11[0],
                state_12[0],state_13[0],state_14[0],state_15[0]]
labels = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15'] #https://matplotlib.org/users/mathtext.html

rtt_list = [state_1[2], state_2[2], state_3[2], state_4[2]*3.5, state_5[2], 
                state_6[2]*1.35, state_7[2]*0.8,state_8[2],state_9[2],state_10[2],state_11[2]*0.5,
                state_12[2]*0.25,state_13[2],state_14[2]*0.25,state_15[2]]

f, ax2 = plt.subplots(nrows=1, ncols=1, figsize=(5,5))
 
labels = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15']

legend = ['RTT']

# Setting the positions and width for the bars
pos = list(range(len(rtt_list)))
width = 0.2 # the width of a bar
    
# Plotting the bars
#fig, ax = plt.subplots(figsize=(10,6))
patterns = ('-', '+', 'x', '\\', '*', 'o', 'O', '.')
plt.plot(labels, rtt_list, 'k',
                 label='Throughput',
                 marker='o',
                 color='black')

plt.show()