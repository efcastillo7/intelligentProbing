#!/usr/bin/env python

'''
 _______     ______  
|_   _\ \   / / ___| 
  | |  \ \ / /\___ \ 
  | |   \ V /  ___) |
  |_|    \_/  |____/ 
Teske Virtual System  
Made by Lucas Teske 
This script reads /proc/net/dev using tools.py to get the data.
The average TX/RX Rates are calculated using an Low Pass Complementary Filter with k
configured as AVG_LOW_PASS. Default to 0.2
This should output something like this on your console:
eth0: in B/S
	RX - MAX: 0 AVG: 0 CUR: 0
	TX - MAX: 0 AVG: 0 CUR: 0
lo: in B/S
	RX - MAX: 1972 AVG: 0 CUR: 0
	TX - MAX: 1972 AVG: 0 CUR: 0
wlan0: in B/S
	RX - MAX: 167658 AVG: 490 CUR: 188
	TX - MAX: 3648202 AVG: 386 CUR: 424
vmnet1: in B/S
	RX - MAX: 0 AVG: 0 CUR: 0
	TX - MAX: 0 AVG: 0 CUR: 0
'''

import time
import math
import sys
sys.path.insert(0, '/home/efcastillo/ryu/ryu/app/intelligentProbing/tools/')
from tools import *

INTERVAL = 1           #   1 second
AVG_LOW_PASS = 0.2      #   Simple Complemetary Filter

ifaces = {}

print "Loading Network Interfaces"
idata = GetNetworkInterfaces()
print "Filling tables"
for eth in idata:
    ifaces[eth["interface"]] = {
        "rxrate"    :   0,
        "txrate"    :   0,
        "avgrx"     :   0,
        "avgtx"     :   0,
        "toptx"     :   0,
        "toprx"     :   0,
        "sendbytes" :   eth["tx"]["bytes"],
        "recvbytes" :   eth["rx"]["bytes"]
    }
    
while True:
    idata = GetNetworkInterfaces()
    for eth in idata:

        if eth["interface"] == "enp3s0":

            #   Calculate the Rate
            ifaces[eth["interface"]]["rxrate"]      =   (eth["rx"]["bytes"] - ifaces[eth["interface"]]["recvbytes"]) / INTERVAL
            ifaces[eth["interface"]]["txrate"]      =   (eth["tx"]["bytes"] - ifaces[eth["interface"]]["sendbytes"]) / INTERVAL
            
            #   Set the rx/tx bytes
            ifaces[eth["interface"]]["recvbytes"]   =   eth["rx"]["bytes"]
            ifaces[eth["interface"]]["sendbytes"]   =   eth["tx"]["bytes"]
            
            #   Calculate the Average Rate
            ifaces[eth["interface"]]["avgrx"]       =   int(ifaces[eth["interface"]]["rxrate"] * AVG_LOW_PASS + ifaces[eth["interface"]]["avgrx"] * (1.0-AVG_LOW_PASS))
            ifaces[eth["interface"]]["avgtx"]       =   int(ifaces[eth["interface"]]["txrate"] * AVG_LOW_PASS + ifaces[eth["interface"]]["avgtx"] * (1.0-AVG_LOW_PASS))
            
            #   Set the Max Rates
            ifaces[eth["interface"]]["toprx"]       =   ifaces[eth["interface"]]["rxrate"] if ifaces[eth["interface"]]["rxrate"] > ifaces[eth["interface"]]["toprx"] else ifaces[eth["interface"]]["toprx"]
            ifaces[eth["interface"]]["toptx"]       =   ifaces[eth["interface"]]["txrate"] if ifaces[eth["interface"]]["txrate"] > ifaces[eth["interface"]]["toptx"] else ifaces[eth["interface"]]["toptx"]
            
            print "%s: in B/S" %(eth["interface"])
            print "\tRX - MAX: %s AVG: %s CUR: %s" %(ifaces[eth["interface"]]["toprx"],ifaces[eth["interface"]]["avgrx"],ifaces[eth["interface"]]["rxrate"])
            print "\tTX - MAX: %s AVG: %s CUR: %s" %(ifaces[eth["interface"]]["toptx"],ifaces[eth["interface"]]["avgtx"],ifaces[eth["interface"]]["txrate"])
            print ""
    time.sleep(INTERVAL) 
