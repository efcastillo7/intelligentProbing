#!/usr/bin/python
"""
Create a network where different switches are connected to
different controllers, by creating a custom Switch() subclass.
"""

from mininet.net import Mininet
from mininet.node import OVSSwitch, Controller, RemoteController, Host
from mininet.topo import SingleSwitchTopo
from mininet.topolib import TreeTopo
from mininet.log import setLogLevel
from mininet.log import info
from mininet.cli import CLI
from mininet.link import Link, TCLink
from mininet.util import custom
from topologies.ufrgstopo import UFRGSTopo
from topologies.fattree import FatTree
from optparse import OptionParser
import time
import sys
import urllib, json
import commands
import os
import pprint
import shutil
import subprocess

# Parameters from shell
parser = OptionParser()
parser.add_option("","--ip",type="string",default="192.168.190.60")
parser.add_option("","--topology",type="string",default="tree")
parser.add_option("","--hosts",type="int",default=8)
parser.add_option("","--depth",type="int",default=3)
parser.add_option("","--fanout",type="int",default=2)
parser.add_option("","--pods",type="int",default=4)

(options, args) = parser.parse_args()
print options

# Verifing topology type
if options.topology == 'tree':
  topo = TreeTopo( depth=options.depth, fanout=options.fanout )
elif options.topology == 'single':
  topo = SingleSwitchTopo( k=options.hosts )
elif options.topology == 'ufrgs':
  topo = UFRGSTopo()
elif options.topology == 'fattree':
  topo = FatTree( num_pods=options.pods )

# Setting mininet configuration
setLogLevel( 'info' )

# Adding root host
root = Host( 'root', inNamespace=False )

# Adding the remote controller
net = Mininet( topo=topo, link=TCLink, autoSetMacs=True, controller=lambda name: RemoteController( name, ip=options.ip ) )

for host in net.hosts:
   host.linkTo ( root )

# Start the network
net.start()

# Waiting for apache starts
file_server = 0
video_server = 1

net.hosts[file_server].cmd('service apache2 restart')
net.hosts[video_server].cmd('su - efcastillo -c \'vlc -vvv /var/www/videoplayback.mp4 --sout "#standard{access=http,mux=asf,dst=:8080}"\' &')
#net.hotst[controller].cmd('sh init_controller.sh')
time.sleep( 10 )

# Hosts requesting the file 
for i in range(0, int(len(net.hosts))):
   if i != 0 and i != 1:
      if (i % 7) == 0:
         net.hosts[i].cmd('./video_request.py ' + str(video_server + 1) + ' &')
      else:
         net.hosts[i].cmd('./file_request.py ' + str(file_server + 1) + ' &') 

print('Topology initialized')
time.sleep( 10 )
#net.pingAll()
#net.hosts[0].cmdPrint( 'ping -i 1 -c 45 ' + net.hosts[120].IP() )
times =10
fo = open("test4_res2_systconapiping.txt", "w")

source = destination = 1
# Hosts requesting the file 
for i in range(0, int(len(net.hosts))):
   if i != 0 and i != 1:
      if (i % 7) == 0:
        source = i
      else:
        destination = i
        
      fo.write(str(net.hosts[source].cmdPrint( 'ping -i 1 -c 45 ' + net.hosts[destination].IP() ) +"\n\n"))

fo.close()
print('Openning console')
CLI( net )
print('Killing process before script ends')
# Kill proccesses before ending script
net.hosts[0].cmd("kill `ps ax | grep file_request | grep -v grep | awk '{print $1}'`")
net.hosts[0].cmd("kill `ps ax | grep video_request | grep -v grep | awk '{print $1}'`")
net.hosts[0].cmd("killall wget")
net.hosts[0].cmd("killall vlc")
print('Done Finish:)')
net.stop()

#https://github.com/phisolani/sdn-openflow1.0-analysis/blob/master/generate_traffic.py 
