class BlockRule:
    pass


class BlockRuleTypeI(BlockRule):
    # Bloquea un paquete de acuerdo a su puerto de destino 
    def __init__(self, destination_ports):
        self.blocked_ports = set(destination_ports)

    def match(self, packet):
        return packet.dst_port in self.blocked_ports


class BlockRuleTypeII(BlockRule):
    # Bloquea un paquete de acuerdo a:
    # - su dirección de origen
    # - su puerto de destino
    # - su protocolo de transporte
    def __init__(self, origin_address, destination_port, transport_protocol):
        self.origin_address = origin_address
        self.destination_port = destination_port
        self.transport_protocol = transport_protocol

    def match(self, packet):
        return packet.src_addr == self.origin_address and \
                packet.dst_port == self.destination_port and \
                packet.transport_protocol == self.transport_protocol


class BlockRuleTypeIII(BlockRule):
    # Bloquea un paquete de acuerdo a:
    # - su dirección de origen
    # - su dirección de destino

    def __init__(self, origin_address, destination_address):
        self.origin_address = origin_address
        self.destination_address = destination_address

    def match(self, packet):
        return packet.src_addr == self.origin_address and \
                packet.dst_addr == self.destination_address
