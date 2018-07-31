from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.topo import Topo
from mininet.link import TCLink
from mininet.topo import SingleSwitchTopo
from mininet.node import RemoteController
import inspect
import os
import atexit

class UFRGSTopo(Topo):
  def __init__(self):
    Topo.__init__(self)
    
    self.host = {}
    for h in range(1,231):
      self.host[h] = self.addHost('h%s' %(h))

    self.switch = {}
    for s in range(1,12):
      self.switch[s] = self.addSwitch('s%s' %(s))
    
    # S1-links to hosts
    for i in range(1,11):
      self.addLink(self.switch[1], self.host[i], cls=TCLink, bw=100)
    
    # S1-links to switches
    self.addLink(self.switch[1], self.switch[2], cls=TCLink, bw=100)
    self.addLink(self.switch[1], self.switch[3], cls=TCLink, bw=100)
    self.addLink(self.switch[1], self.switch[7], cls=TCLink, bw=100)
    self.addLink(self.switch[1], self.switch[11], cls=TCLink, bw=100)
    
    # S2-links to hosts
    for i in range(11,51):   
      self.addLink(self.switch[2], self.host[i], cls=TCLink, bw=100)
   
    # S3-links to hosts
    for i in range(51,71):
      self.addLink(self.switch[3], self.host[i], cls=TCLink, bw=100)

    # S3-links to switches
    self.addLink(self.switch[3], self.switch[4], cls=TCLink, bw=100)
    self.addLink(self.switch[3], self.switch[5], cls=TCLink, bw=100)

    # S4-links to hosts
    for i in range(71,81):
      self.addLink(self.switch[4], self.host[i], cls=TCLink, bw=100)

    # S5-links to hosts
    for i in range(81,111):
      self.addLink(self.switch[5], self.host[i], cls=TCLink, bw=100)
 
    # S6-links to hosts
    for i in range(111,121):
      self.addLink(self.switch[6], self.host[i], cls=TCLink, bw=100)
  
    # S6-links to switches
    self.addLink(self.switch[6], self.switch[7], cls=TCLink, bw=100)

    # S7-links to hosts
    for i in range(121,141):
      self.addLink(self.switch[7], self.host[i], cls=TCLink, bw=100)
 
    # S7-links to switches
    self.addLink(self.switch[7], self.switch[8], cls=TCLink, bw=100)
    self.addLink(self.switch[7], self.switch[9], cls=TCLink, bw=100)

    # S8-links to hosts
    for i in range(141,151):
      self.addLink(self.switch[8], self.host[i], cls=TCLink, bw=100)

    # S9-links to hosts
    for i in range(151,171):
      self.addLink(self.switch[9], self.host[i], cls=TCLink, bw=100)
   
    # S10-links to hosts
    for i in range(171,211):
      self.addLink(self.switch[10], self.host[i], cls=TCLink, bw=100)

    # S11-links to hosts
    for i in range(211,231):
      self.addLink(self.switch[11], self.host[i], cls=TCLink, bw=100)
    
    # S11-links to switches
    self.addLink(self.switch[11], self.switch[10], cls=TCLink, bw=100)

#topos = {'ufrgstopo':(lambda:UFRGSTopo())}

def startNetwork():
    info('** Creating Overlay network topology\n')
    topo = UFRGSTopo()
    global net
    net = Mininet(topo=topo, link = TCLink,
                  controller=lambda name: RemoteController(name, ip='143.54.12.113'),
                  listenPort=6633, autoSetMacs=True)

    info('** Starting the network\n')
    net.start()

    """
    count = len(net.hosts)
    for i in range(0, int(len(net.hosts))):
      print("Modulo 7...")
      net.hosts[ i ].cmd( 'iperf -s -u -i 1 &' )

    i = 0
    for j in range(0, int(len(net.hosts))):
      i = ( i + 1 ) % count
      ip = net.hosts[ i ].IP()
      print("Modulo Cliente...", ip)
      net.hosts[ i ].sendCmd( 'iperf -u -b 1m -n 1000 -c ' + ip )
    """

    net.pingAll()
    """
    countx = 0
    for i in range(0, int(len(net.hosts))):
      if i != 0 and i != 1:
        if (i % 7) == 0:
          print("Modulo 7...", net.hosts[i].IP())
          countx += 1
          #net.hosts[i].cmd('iperf -s &')
        else:
          net.hosts[i].sendCmd('iperf -t 99999 -i 1 -c' + net.hosts[i].IP())
          print("Modulo xxx...", net.hosts[i].IP())
"""

    info('** Running CLI\n')
    CLI(net)

def waiting( self ):
        "Are we waiting for output?"
        return self.node.waiting

def stopNetwork():
    if net is not None:
        info('** Tearing down Overlay network\n')
        #net.hosts[0].cmd("pkill -9 iperf")
        #net.hosts[0].cmd("kill %iperf")
        net.stop()

if __name__ == '__main__':
    # Force cleanup on exit by registering a cleanup function
    atexit.register(stopNetwork)

    # Tell mininet to print useful information
    setLogLevel('info')
    startNetwork()
