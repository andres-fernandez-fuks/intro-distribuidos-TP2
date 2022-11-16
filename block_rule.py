import pox.lib.packet as pkt
from pox.lib.addresses import EthAddr


class BlockRule:
    pass


class BlockRuleTypeI(BlockRule):
    # Bloquea un paquete de acuerdo a su puerto de destino 
    def __init__(self, destination_port):
        self.blocked_port = destination_port

    def create_rules(self):
        # A single BlockRule can translate into multiple pox rules
        rule_1 = {'tp_dst': self.blocked_port, 'nw_proto': pkt.ipv4.TCP_PROTOCOL, 'dl_type': pkt.ethernet.IP_TYPE}
        rule_2 = {'tp_dst': self.blocked_port, 'nw_proto': pkt.ipv4.UDP_PROTOCOL, 'dl_type': pkt.ethernet.IP_TYPE}
        # No es necesario bloquear ICMP porque no tiene puerto de destino
        return [rule_1, rule_2]
         


class BlockRuleTypeII(BlockRule):
    # Bloquea un paquete de acuerdo a:
    # - su direccion de origen
    # - su puerto de destino
    # - su protocolo de transporte
    def __init__(self, origin_address, destination_port, transport_protocol):
        self.origin_address = origin_address
        self.destination_port = destination_port
        self.transport_protocol = transport_protocol

    def create_rules(self):
        rule_1 = {
            'dl_src': EthAddr('00:00:00:00:00:0{}'.format(self.origin_address)),
            'dl_type': pkt.ethernet.IP_TYPE,
            'tp_dst': self.destination_port,
            'nw_proto': self.transport_protocol
        }
        return [rule_1]


class BlockRuleTypeIII(BlockRule):
    # Bloquea un paquete de acuerdo a:
    # - su direccion de origen
    # - su direccion de destino

    def __init__(self, origin_address, destination_address):
        self.origin_address = origin_address
        self.destination_address = destination_address

    def create_rules(self):
        rule_1 = {
            'dl_src': EthAddr('00:00:00:00:00:0{}'.format(self.origin_address)),
            'dl_dst': EthAddr('00:00:00:00:00:0{}'.format(self.destination_address)),
            'dl_type': pkt.ethernet.IP_TYPE,
        }
        rule_2 = {
            'dl_src': EthAddr('00:00:00:00:00:0{}'.format(self.destination_address)),
            'dl_dst': EthAddr('00:00:00:00:00:0{}'.format(self.origin_address)),
            'dl_type': pkt.ethernet.IP_TYPE,
        }
        return [rule_1, rule_2]
