import pox.lib.packet as pkt

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from collections import namedtuple
from pox.lib.revent import EventMixin
import os
import settings

# Add your imports here ...
log = core.getLogger()

# Add your global variables here ...
class Firewall(EventMixin):
    def __init__(self):
        self.listenTo(core.openflow)
        log.debug("Enabling Firewall Module")
    
    def _handleConnectionUp(self, event):

        import pdb; pdb.set_trace()
        # if event.connection.dpid != settings.FIREWALL_DPID:
        #     return

        log.debug(f"Switch {event.dpid} has come up.")
        
        # rule = {'nw_proto': pkt.ipv4.ICMP_PROTOCOL}
        rule = {'nw_src': '10.0.0.1'}

        match = of.ofp_match(**rule)
        msg = of.ofp_flow_mod(match=match)
        event.connection.send(msg)


    def launch():
        # Starting the Firewall module
        core.registerNew ( Firewall )

