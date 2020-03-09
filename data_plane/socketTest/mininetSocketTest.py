#!/usr/bin/python
#https://gist.github.com/dufferzafar

from mininet.node import OVSController

from mininet.topo import SingleSwitchTopo
from mininet.net import Mininet
from mininet.log import lg
from mininet.cli import CLI


def main():
    lg.setLogLevel('info')

    net = Mininet(SingleSwitchTopo(k=2), controller=OVSController)
    net.start()

    h1 = net.get('h1')
    p1 = h1.popen('python myServer.py -i %s &' % h1.IP())

    h2 = net.get('h2')
    h2.cmd('python myClient.py -i %s -m "hello world"' % h1.IP())

    CLI(net)
    p1.terminate()
    net.stop()

if __name__ == '__main__':
    main()