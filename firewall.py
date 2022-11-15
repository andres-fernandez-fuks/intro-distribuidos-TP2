# pox
import pox.lib.packet as pkt
import pox.openflow.libopenflow_01 as of
from pox.core import core
from pox.lib.revent import EventMixin


#internal files
import settings
import block_rule as br

log = core.getLogger()


class Firewall(EventMixin):
    def __init__(self):
        self.listenTo(core.openflow)
        log.debug("Habilitando Firewall")


    def create_rules(self):
        type_I_rules = br.BlockRuleTypeI(settings.R1_BLOCKED_DST_PORT).create_rules()
        type_II_rules = br.BlockRuleTypeII(settings.R2_BLOCKED_SRC_ADDR, settings.R2_BLOCKED_DST_PORT, settings.R2_BLOCKED_PROTOCOL).create_rules()
        type_III_rules = br.BlockRuleTypeIII(settings.R3_BLOCKED_SRC_ADDR, settings.R3_BLOCKED_DST_ADDR).create_rules()
        return type_I_rules + type_II_rules + type_III_rules


    def _handle_ConnectionUp(self, event):
        if (event.connection.dpid != settings.FIREWALL_SWITCH_ID):
            return
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
            log.info(' ----------------------------')
            log.info(" Nuevo Paquete IP:")
            packet_payload = ip_packet.payload
            log.info("  IP Origen: {}".format(ip_packet.srcip))
            log.info("  IP Destino: {}".format(ip_packet.dstip))
            if ip_packet.protocol == ip_packet.TCP_PROTOCOL:
                log.info("  Protocolo: TCP")
            elif ip_packet.protocol == ip_packet.UDP_PROTOCOL:
                log.info("  Protocolo: UDP")
            elif ip_packet.protocol == ip_packet.ICMP_PROTOCOL:
                log.info("  Protocolo: ICMP")
                return # si es ICMP no se puede acceder a srcport y dstport
            log.info("  Puerto Origen: {}".format(packet_payload.srcport))
            log.info("  Puerto Destino: {}".format(packet_payload.dstport))
            log.info(' ----------------------------')

def launch():
    """
    Starting the Firewall Module
    """
    core.registerNew(Firewall)
