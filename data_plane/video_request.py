#!/usr/bin/python
import urllib2
import random
import time
import subprocess
import sys

roust = sys.argv[1]
print(roust)

i = 1
while (i == 1):
   random_number = random.expovariate(0.033)
   time.sleep(random_number) 
   # cvlc -vvv chulapa.mp4 --sout '#standard{access=http,mux=asf,dst=:8080}'
   a = subprocess.Popen(['sudo su - efcastillo -c "expect vlc_stream.x ' + roust + '"'], shell=True)
   #time.sleep(10)
   # a.terminate()
   a.wait()
   #response = urllib2.urlopen('http://10.0.0.2/arquivoMedio.html')
   print ("From Video")
   #html_string = response.read()

