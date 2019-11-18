#!/usr/bin/python

"""

"""

import inspect
import os
import atexit
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.topo import Topo
from mininet.link import TCLink
from mininet.topo import SingleSwitchTopo
from mininet.node import RemoteController

import time
import sys
import urllib, json
import commands
import os
import pprint
import shutil
import subprocess
import requests


net = None

class FVTopo(Topo):
    # credit: https://github.com/onstutorial/onstutorial/blob/master/flowvisor_scripts/flowvisor_topo.py
    def __init__(self):
        # Initialize topology
        Topo.__init__(self)

        # Create template host, switch, and link
        hconfig = {'inNamespace':True}
        http_link_config = {'bw': 1}
        video_link_config = {'bw': 10}
        host_link_config = {}

        # Create switch nodes
        for i in range(4):
            sconfig = {'dpid': "%016x" % (i+1)}
            self.addSwitch('s%d' % (i+1), **sconfig)

        # Create host nodes
        for i in range(4):
            self.addHost('h%d' % (i+1), **hconfig)

        # Add switch links
        # Specified to the port numbers to avoid any port number consistency issue
        
        self.addLink('s2', 's1', port1=1, port2=1, **http_link_config)
        self.addLink('s3', 's1', port1=1, port2=2, **video_link_config)
        self.addLink('h1', 's1', port1=1, port2=3, **host_link_config)
        self.addLink('h2', 's1', port1=1, port2=4, **host_link_config)
        
        self.addLink('s2', 's4', port1=2, port2=1, **http_link_config)
        self.addLink('s3', 's4', port1=2, port2=2, **video_link_config)
        self.addLink('h3', 's4', port1=1, port2=3, **host_link_config)
        self.addLink('h4', 's4', port1=1, port2=4, **host_link_config)
        
        info( '\n*** printing and validating the ports running on each interface\n' )
        


def startNetwork():
    info('** Creating Overlay network topology\n')
    topo = FVTopo()
    global net
    net = Mininet(topo=topo, link = TCLink,
                  controller=lambda name: RemoteController(name, ip='143.54.12.113'),
                  listenPort=6633, autoSetMacs=True)

    

    info('** Starting the network\n')
    net.start()

    # Waiting for apache starts
    file_server = 0
    video_server = 1

    net.hosts[file_server].cmd('service apache2 restart')
    net.hosts[video_server].cmd('su - pedro -c \'vlc -vvv /var/www/chulapa.mp4 --sout "#standard{access=http,mux=asf,dst=:8080}"\' &')

    time.sleep( 10 )

    # Hosts requesting the file 
    for i in range(0, int(len(net.hosts))):
       if i != 0 and i != 1:
          if (i % 7) == 0:
             net.hosts[i].cmd('./video_request.py ' + str(video_server + 1) + ' &')         



    info('** Running CLI\n')
    CLI(net)


def stopNetwork():
    if net is not None:
        info('** Tearing down Overlay network\n')
        net.hosts[0].cmd("kill `ps ax | grep file_request | grep -v grep | awk '{print $1}'`")
        net.hosts[0].cmd("kill `ps ax | grep video_request | grep -v grep | awk '{print $1}'`")
        net.hosts[0].cmd("killall wget")
        net.hosts[0].cmd("killall vlc")
        net.stop()


if __name__ == '__main__':
    # Force cleanup on exit by registering a cleanup function
    atexit.register(stopNetwork)

    # Tell mininet to print useful information
    setLogLevel('info')
    startNetwork()