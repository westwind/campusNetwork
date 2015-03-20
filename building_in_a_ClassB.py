#!/usr/bin/python

from mininet.cli import CLI
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost, Controller, RemoteController
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel

# Level: building, floor and room
# There are mash between buildings
# each building is tree topology

class CampusTopo(Topo):
    def __init__(self, building=2, floor=2, room=2, host=2, **opts):
        Topo.__init__(self, **opts)
        #create root switch of building
        for b in range(building):
            switch = self.addSwitch( 's%s' %(b+1) )

        # create switches for each floor
        for b in range(building):
            for f in range(floor):
                rootswitch = ('s%s' %(b+1))
                switch = self.addSwitch( 's%s%s' %(b+1,f+1) )
                self.addLink(switch, rootswitch)

        for b in range(building):
                for f in range(floor):
                    for r in range(room):
                        floorswitch = ( 's%s%s' %(b+1,f+1))
                        switch = self.addSwitch( 's%s%s%s' %(b+1,f+1,r+1) )
                        self.addLink(switch, floorswitch)

        for b in range(1,building+1):
            gateway =  '172.16.0.254'
            ip = 1
            for f in range(1,floor+1):
                for r in range(1,room+1):
                    for h in range(1,host+1):
                        roomswitch = ( 's%s%s%s' %(b,f,r))
                        computer = self.addHost('h%s%s%s%s' % (b,f,r,h), 
                                    ip='172.16.%d.%d/16' % (b,ip),
                                    defaultRoute='via %s' % gateway)
                        ip = ip + 1
                        self.addLink(computer, roomswitch)

### simple link between root switch ###
#       for b in range(1,building):
#           switch1 = ( 's%s' %(b))
#           switch2 = ( 's%s' %(b+1))
#           self.addLink(switch1, switch2)

#### mash ####
        for b in range(1,building):
            for x in range(b+1,building+1):
                switch1 = ( 's%s' %(b))
                switch2 = ( 's%s' %(x))
                self.addLink(switch1, switch2)

def simpleTest():
    topo = CampusTopo(building=3,floor=2,room=2,host=1)
    net = Mininet(topo, controller=RemoteController( 'c0', ip='127.0.0.1' ))
    net.start()
    print("Dumping host connections")
    dumpNodeConnections(net.hosts)
    print("Testing network connectivity")
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    simpleTest()
