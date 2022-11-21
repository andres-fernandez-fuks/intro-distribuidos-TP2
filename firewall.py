# pox
import pox.lib.packet as pkt
import pox.openflow.libopenflow_01 as of
from pox.core import core
from pox.lib.revent import EventMixin
from pox.lib.util import dpid_to_str


# internal files
import settings
import block_rule as br

log = core.getLogger()


class Firewall(EventMixin):
    def __init__(self):
        self.listenTo(core.openflow)
        log.debug("Habilitando Firewall")

    def create_rules(self):
        rules = []
        for block_rule in settings.ACTIVE_RULES:
            rules += block_rule.create_rules()
            if block_rule.should_raise_warning():
                log.warning("Advertencia: {}".format(block_rule.get_warning()))
        return rules

    def _handle_ConnectionUp(self, event):
        if event.connection.dpid != settings.FIREWALL_SWITCH_ID:
            return
        event_mac_address = dpid_to_str(event.connection.dpid)
        log.info("El switch con direccion %s aplicara las reglas", event_mac_address)
        rules = self.create_rules()
        for rule in rules:
            log.info(" Aplicando regla: {}".format(rule))
            match = of.ofp_match(**rule)
            msg = of.ofp_flow_mod(match=match)
            event.connection.send(msg)

    def _handle_PacketIn(self, event):
        packet = event.parsed
        if packet.type == packet.IP_TYPE:
            ip_packet = packet.payload
            packet_payload = ip_packet.payload
            log.info(" IP SRC{}".format(ip_packet.srcip))
            log.info(" IP DST: {}".format(ip_packet.dstip))
            if ip_packet.protocol == ip_packet.TCP_PROTOCOL:
                log.info(" TCP Protocol")
            elif ip_packet.protocol == ip_packet.UDP_PROTOCOL:
                log.info(" UDP Protocol")
            elif ip_packet.protocol == ip_packet.ICMP_PROTOCOL:
                log.info(" ICMP Protocol")
                return  # si es ICMP no se puede acceder a srcport y dstport
            log.info(" PORT SRC: {}".format(packet_payload.srcport))
            log.info(" PORT DST: {}".format(packet_payload.dstport))
            log.info(" #########################")


def launch():
    """
    Starting the Firewall Module
    """
    core.registerNew(Firewall)
