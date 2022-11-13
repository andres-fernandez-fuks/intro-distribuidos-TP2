from mininet.topo import Topo

class CustomTopology(Topo):
    HOSTS_AMOUNT = 2


    def __init__(self, switch_amount):
        Topo.__init__(self)
        hosts = self.add_hosts()
        switches = self.add_switches(switch_amount)
        self.add_links(hosts, switches)


    def add_hosts(self):
        hosts = []
        for i in range(self.HOSTS_AMOUNT):
            hosts.append(self.addHost('h' + str(i+1)))
        return hosts


    def add_switches(self, switch_amount):
        switches = []
        for i in range(switch_amount):
            switches.append(self.addSwitch('s' + str(i+1)))
        return switches


    def add_links_between_hosts_and_switches(self, hosts, switches):
        for host in hosts:
            for switch in switches:
                self.addLink(host, switch)


    def add_links_between_switches(self, switches):
        for i, switch in enumerate(switches[:-1]):
            self.addLink(switch, switches[i+1])


    def add_links(self, hosts, switches):
        self.add_links_between_hosts_and_switches(hosts, switches)
        self.add_links_between_switches(switches)


topos = { 'custom': CustomTopology }