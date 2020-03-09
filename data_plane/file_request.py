#!/usr/bin/python
import urllib2
import random
import time
import subprocess
import sys

rost = sys.argv[1]
i = 1
while (i == 1):
   random_number = random.expovariate(0.033)
   time.sleep(random_number)
   a = subprocess.Popen(['/usr/bin/wget', '--delete-after', 'http://10.0.0.' + rost + '/arquivo.html'])
   a.wait()
   #time.sleep(4)
   #response = urllib2.urlopen('http://10.0.0.2/arquivoMedio.html')
   print 'Request file'
   #html_string = response.read()

