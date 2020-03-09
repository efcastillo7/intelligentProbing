#!/usr/bin/python

"""
This script fires up a fat tree topology with mininet
"""

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.log import setLogLevel, info
from mininet.cli import CLI

class Ring(Topo):
    """
    Creates a ring topology
    """

    def __init__(self, num_switches=4):
        Topo.__init__(self)

        switches = []
        sindex = 0
        for i in range(0, num_switches):
            sindex += 1
            switches.append(self.addSwitch('as' + str(sindex)))

        sindex = 0
        for i in range(0, num_switches):
            self.addLink(switches[sindex], switches[sindex-1])
            h = self.addHost('h' + str(sindex + 1))
            self.addLink(switches[sindex], h)
            sindex += 1
            

class FatTree(Topo):
    """
    Creates a FatTree topology according to Al-Fares et al. 
    "A Scalable, Commodity Data Center Network Architecture"
    SIGCOMM'08
    """

    def __init__(self, num_pods=4):
        Topo.__init__(self)

        # Add edge and aggregation switches
        pods = {}
        sindex = 0
        hindex = 0
        for i in range(num_pods):
            current_pod = 'p' + str(i)
            pods[current_pod] = {
                'edge_switches': [], 
                'aggregation_switches': [], 
                'hosts': []
            }
            # There are pods/2 edge and aggregation switches per pod
            for j in range(num_pods/2):
                sindex += 1
                edpid = self.makeDpid(1, sindex)
                adpid = self.makeDpid(2, sindex)
                pods[current_pod]['edge_switches'].append(self.addSwitch('es' + str(sindex), dpid = edpid))
                pods[current_pod]['aggregation_switches'].append(self.addSwitch('as' + str(sindex), dpid = adpid))

                # Add pods/2 hosts and connect to edge switches
                for k in range(num_pods/2):
                    hindex += 1
                    pods[current_pod]['hosts'].append(self.addHost('h' + str(hindex)))
                    self.addLink(
                        pods[current_pod]['edge_switches'][j],
                        pods[current_pod]['hosts'][((num_pods/2)*j)+k]
                    )
        
        # Connect edge to aggregation switches
        for pod in pods:
            # Each edge switch is connected to every aggregation switch inside a pod
            for esw in pods[pod]['edge_switches']:
                for asw in pods[pod]['aggregation_switches']:
                    self.addLink(esw, asw)

        # Add (k/2)^2 core switches
        cindex = 0
        core_switches = []
        for i in range((num_pods/2)**2):
            cindex += 1
            core_switches.append(self.addSwitch('cs' + str(cindex), dpid = self.makeDpid(3, cindex)))
            # Every core switch connects to one aggregation switch in every pod
            for pod in pods:
                link_index = (cindex-1)/(num_pods/2)
                self.addLink(core_switches[cindex-1], pods[pod]['aggregation_switches'][link_index])


    # This will make a representation of the switch dpid showing the layer (core, edge, aggr) and switch_id
    def makeDpid(self, layer, switch_id):
        # Layer info is shifted 4 bytes to the left
        return str(layer).zfill(8) + str(switch_id).zfill(8)


def startTopo():

    topology = FatTree(num_pods = 12)
    #topology = Ring()
    net = Mininet(topo=topology, controller=RemoteController, autoSetMacs=True, build=False)
    
    info('*** Adding controller\n')
    net.addController('c0', controller=RemoteController, ip='143.54.12.45')
    
    info( '*** Building network\n')
    net.build()
    
    info( '*** Starting network\n')
    net.start()
    
    info( '*** Running CLI\n' )
    CLI( net )
    
    info( '*** Stopping network' )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    startTopo()
