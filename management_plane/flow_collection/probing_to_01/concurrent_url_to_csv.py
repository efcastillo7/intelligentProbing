#!/usr/bin/env python
import eventlet
import requests
import csv
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib as style
import numpy as np
import sys
sys.path.insert(0, '/home/efcastillo/ryu/ryu/app/intelligentProbing/tools/')
from dynamic_plot import *

#plt.style.use('fivethirtyeight')

#s_no=1
flag=1
count_iter=0

xdata = []
ydata_aux = []
ydata = []
zdata_aux = []
zdata = []
"""
plt.show()
 
axes = plt.gca()
axes.set_xlim(0, 100)
axes.set_ylim(0, 50000)
line, = axes.plot(xdata, ydata, 'r-')
"""
s=requests.Session()
baseurl='http://143.54.12.113:8080/stats/'
switches_url=baseurl+'switches'
switch_list=s.get(switches_url)

files_list=['aggregateflow']
urls = []
sl=switch_list.json()
for i in files_list:
	for s_no in switch_list.json():
		#fp=open(i+'_'+str(s_no)+'.csv', 'a')
		urls += [baseurl+i+'/'+str(s_no)]

def fetch(url):
#print("opening", url)
	global flag
	r = s.get(url)
	body=r.json()
	sno=url[-1]
	data=body[sno]
	print(type(data))
	#data.append({'Fer':count_iter})	
	fp=open(url[len(baseurl):-2]+'_'+sno+'.csv', 'a')
	if fp.tell()==0:
		flag=0
	csvwriter=csv.writer(fp)
	for item in data:
		#print(item["packet_count"])
		if flag == 0:
			csvwriter.writerow(item.keys())
			flag=1		
		csvwriter.writerow(item.values())
		ydata_aux.append(item["packet_count"])
		zdata_aux.append(item["byte_count"])
	#print(ydata)
	return url

pool = eventlet.GreenPool(200)
while(1):
	for url in pool.imap(fetch, urls):		
 		time.sleep(0.1)
 	
	
	xdata.append(count_iter)
	ydata.append(int(sum(ydata_aux)/len(ydata_aux)))
	zdata.append(int(sum(zdata_aux)/len(zdata_aux)))
	#print(zdata)
	d = DynamicUpdate(xdata,zdata)
	

	#line.set_xdata(xdata)
	#line.set_ydata(ydata)
	#plt.draw()
	#plt.pause(1e-17)
	#time.sleep(0.1)	
	
	
	count_iter += 1
#plt.show()
