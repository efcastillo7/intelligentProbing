import sys
sys.path.insert(0, '/home/efcastillo/ryu/ryu/app/intelligentProbing/tools/')
from statistics import mean, stdev
from os import scandir, getcwd
import os.path as path
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
    		print ('Line {i} is corrupt!'.format(i = i))
    		pass
    
    Minimun = round(min(rtt),3)
    Maximun = round(max(rtt),3)
    Mean = round(mean(rtt),3)
    Desv = round(stdev(rtt),3) 	
    return [Minimun, Maximun, Mean, Desv]

currentPath = getcwd()
print(currentPath)

state_1 = csvRead(currentPath + '/pcap/probing_1s-rtt.csv')
print(state_1)

#print ("Min ", round(min(rtt),3), " Max ", round(max(rtt),3))
#print ("Mean ", round(mean(rtt),3), "Desv ", round(stdev(rtt),3))

#rtt.append(float(iRTT)*1000)
