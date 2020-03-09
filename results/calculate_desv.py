import sys
sys.path.insert(0, '/home/efcastillo/ryu/ryu/app/intelligentProbing/tools/')
from statistics import mean, stdev
from os import scandir, getcwd
import os.path as path
import numpy as np
from matplotlib import pyplot
from pathlib import Path
import csv


def csvRead(csv_file):    

    if not path.exists(csv_file):
            print("The file does not exist")
            sys.exit()
    rtt = []
    Minimun = Maximun = Mean = Desv = 0
    for i, row in enumerate(csv.reader(open(csv_file, 'r', encoding='utf-8'))):
    	if not i or not row:
    		continue
    	_,_,_,_,_,_,_,iRTT,_ = row

    	try:
    		rtt.append(float(iRTT)*1000)
    	except Exception as e:
    		print ('Line {i} is corrupt!'.format(i = i), " File ", Path(csv_file).name)
    		pass
    
    Minimun = round(min(rtt),3)
    Maximun = round(max(rtt),3)
    Mean = round(mean(rtt),3)
    Desv = round(stdev(rtt),3)
    return [Minimun, Maximun, Mean, Desv]

currentPath = getcwd()
print(currentPath)


state_05 = csvRead(currentPath + '/pcap/probing_05s-rtt.csv')
state_1 = csvRead(currentPath + '/pcap/probing_1s-rtt.csv')
state_2 = csvRead(currentPath + '/pcap/probing_2s-rtt.csv')
state_3 = csvRead(currentPath + '/pcap/probing_3s-rtt.csv')
state_4 = csvRead(currentPath + '/pcap/probing_4s-rtt.csv')
state_5 = csvRead(currentPath + '/pcap/probing_5s-rtt.csv')
state_6 = csvRead(currentPath + '/pcap/probing_6s-rtt.csv')
state_7 = csvRead(currentPath + '/pcap/probing_7s-rtt.csv')
state_8 = csvRead(currentPath + '/pcap/probing_8s-rtt.csv')
state_9 = csvRead(currentPath + '/pcap/probing_9s-rtt.csv')
state_10 = csvRead(currentPath + '/pcap/probing_10s-rtt.csv')
state_11 = csvRead(currentPath + '/pcap/probing_11s-rtt.csv')
state_12 = csvRead(currentPath + '/pcap/probing_12s-rtt.csv')
state_13 = csvRead(currentPath + '/pcap/probing_13s-rtt.csv')
state_14 = csvRead(currentPath + '/pcap/probing_14s-rtt.csv')
state_15 = csvRead(currentPath + '/pcap/probing_15s-rtt.csv')

means = [state_05[2], state_1[2], state_2[2], state_3[2], state_4[2], state_5[2], 
                state_6[2], state_7[2],state_8[2],state_9[2],state_10[2],state_11[2],
                state_12[2],state_13[2],state_14[2],state_15[2]]

#peakval = [str(state_05[2]),str( state_1[2]),str( state_2[2]),str( state_3[2]),str( state_4[2]),str( state_5[2]), 
#               str(state_6[2]),str( state_7[2]),str(state_8[2]),str(state_9[2]),str(state_10[2]),str(state_11[2]),
#                str(state_12[2]),str(state_13[2]),str(state_14[2]),str(state_15[2])]                

stds_list = [state_05[3], state_1[3], state_2[3], state_3[3], state_4[3], state_5[3], 
                state_6[3], state_7[3],state_8[3],state_9[3],state_10[3],state_11[3],
                state_12[3],state_13[3],state_14[3],state_15[3]]

labels = ['0.5','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15']
#means   = [26.82,26.4,61.17,61.55]           # Mean Data 
stds    = [(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0), stds_list] # Standard deviation Data
peakval = ['','','','','','','','','','','','','','','','']   # String array of means

ind = np.arange(len(means))
width = 0.35
#colours = ['red','blue','green','yellow']

pyplot.figure()
#pyplot.title('Average Age')
pyplot.bar(ind, means, width, color="w", align='center', yerr=stds, ecolor='k', edgecolor='black', hatch='xxx')
pyplot.ylabel('Round Trip Time (ms)')
pyplot.xlabel('Monitoring Interval (s)')
pyplot.xticks(ind,labels)
pyplot.tight_layout()
pyplot.grid()

def autolabel(bars,peakval):
    for ii,bar in enumerate(bars):
        height = bars[ii]
        pyplot.text(ind[ii], height+0.2, '%s'% (peakval[ii]), ha='center', va='top')
autolabel(means,peakval) 
pyplot.show()