from mininet.topo import Topo
from mininet.link import TCLink

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

topos = {'ufrgstopo':(lambda:UFRGSTopo())}
