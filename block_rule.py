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
        rule_1 = {
            "tp_dst": self.blocked_port,
            "nw_proto": pkt.ipv4.TCP_PROTOCOL,
            "dl_type": pkt.ethernet.IP_TYPE,
        }
        rule_2 = {
            "tp_dst": self.blocked_port,
            "nw_proto": pkt.ipv4.UDP_PROTOCOL,
            "dl_type": pkt.ethernet.IP_TYPE,
        }
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
            "dl_src": EthAddr("00:00:00:00:00:0{}".format(self.origin_address)),
            "dl_type": pkt.ethernet.IP_TYPE,
            "tp_dst": self.destination_port,
            "nw_proto": self.transport_protocol,
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
            "dl_src": EthAddr("00:00:00:00:00:0{}".format(self.origin_address)),
            "dl_dst": EthAddr("00:00:00:00:00:0{}".format(self.destination_address)),
            "dl_type": pkt.ethernet.IP_TYPE,
        }
        rule_2 = {
            "dl_src": EthAddr("00:00:00:00:00:0{}".format(self.destination_address)),
            "dl_dst": EthAddr("00:00:00:00:00:0{}".format(self.origin_address)),
            "dl_type": pkt.ethernet.IP_TYPE,
        }
        return [rule_1, rule_2]


class GenericBlockRule(BlockRule):
    def __init__(self, restrictions):
        self.blocked_protocol = restrictions.get("protocol", None)
        self.blocked_src_host = restrictions.get("src_host", None)
        self.blocked_src_port = restrictions.get("src_port", None)
        self.blocked_dst_host = restrictions.get("dst_host", None)
        self.blocked_dst_port = restrictions.get("dst_port", None)

    def get_blocked_src_host_address(self):
        return (
            EthAddr("00:00:00:00:00:0{}".format(self.blocked_src_host))
            if self.blocked_src_host
            else None
        )

    def get_blocked_dst_host_address(self):
        return (
            EthAddr("00:00:00:00:00:0{}".format(self.blocked_dst_host))
            if self.blocked_dst_host
            else None
        )

    def create_rules(self):
        if self.is_rule_between_specific_hosts():
            return self.create_rules_between_specific_hosts()
        return self.create_rules_between_any_hosts()

    def is_rule_between_specific_hosts(self):
        # Si se especifican los dos hosts (como en la regla 3), la regla es un poco distinta
        return self.blocked_src_host and self.blocked_dst_host

    def create_rules_between_specific_hosts(self):
        # Crea las reglas cuando ambos hosts son especificados
        rules_for_src = self.create_rules_between_specific_hosts_for_host(is_source=True)
        rules_for_dst = self.create_rules_between_specific_hosts_for_host(is_source=False)
        return rules_for_src + rules_for_dst

    def create_rules_between_specific_hosts_for_host(self, is_source):
        # crea las reglas para un host en particular
        if self.port_specified_but_not_protocol(is_source):
            return self.create_rules_between_specific_hosts_with_port_for_host(
                is_source
            )
        if self.blocked_protocol:
            return self.create_rules_between_specific_hosts_with_port_and_protocol_for_host(
                is_source
            )
        return self.create_rules_between_specific_hosts_with_only_host(is_source)

    def get_parameters_for_specific_hosts(self, is_source):
        if is_source:
            dl_src = self.get_blocked_src_host_address()
            dl_dst = self.get_blocked_dst_host_address()
            tp_src = self.blocked_src_port
            tp_dst = self.blocked_dst_port
        else:
            dl_src = self.get_blocked_dst_host_address()
            dl_dst = self.get_blocked_src_host_address()
            tp_src = self.blocked_dst_port
            tp_dst = self.blocked_src_port
        return (
            dl_src,
            dl_dst,
            tp_src,
            tp_dst,
        )  # No tiene sentido bloquear en base al tp_src, no se puede definir

    def create_rules_between_specific_hosts_with_port_for_host(self, is_source=True):
        # Se especifica un puerto, pero no un protocolo. Como el protocolo no puede ser None, hay que hacer dos reglas.
        # Se llama for_host para que quede mas claro que es para un solo host
        dl_src, dl_dst, tp_src, tp_dst = self.get_parameters_for_specific_hosts(
            is_source
        )
        rule_1 = {
            "dl_src": dl_src,
            "dl_dst": dl_dst,
            "dl_type": pkt.ethernet.IP_TYPE,
            "tp_src": tp_src,
            "tp_dst": tp_dst,
            "nw_proto": pkt.ipv4.UDP_PROTOCOL,
        }
        rule_2 = {
            "dl_src": dl_src,
            "dl_dst": dl_dst,
            "dl_type": pkt.ethernet.IP_TYPE,
            "tp_src": tp_src,
            "tp_dst": tp_dst,
            "nw_proto": pkt.ipv4.TCP_PROTOCOL,
        }
        return [rule_1, rule_2]

    def create_rules_between_specific_hosts_with_only_host(self, is_source=True):
        # Para un host en particular, se especifica solamente bloquear la direccion IP
        dl_src, dl_dst, _ = self.get_parameters_for_specific_hosts(is_source)
        rule_1 = {
            "dl_src": dl_src,
            "dl_dst": dl_dst,
            "dl_type": pkt.ethernet.IP_TYPE,
            "tp_src": None,
            "tp_dst": None,
            "nw_proto": None,
        }
        return [rule_1]

    def create_rules_between_specific_hosts_with_port_and_protocol_for_host(
        self, is_source=True
    ):
        # Se especifican host, puerto y protocolo (todo lo posible)
        # Se llama for_host para que quede mas claro que es para un solo host
        dl_src, dl_dst, tp_src, tp_dst = self.get_parameters_for_specific_hosts(
            is_source
        )
        rule_1 = {
            "dl_src": dl_src,
            "dl_dst": dl_dst,
            "dl_type": pkt.ethernet.IP_TYPE,
            "tp_src": tp_src,
            "tp_dst": tp_dst,
            "nw_proto": self.blocked_protocol,
        }
        return [rule_1]

    def any_port_specified_but_not_protocol(self):
        # Si se especifica alguno de los dos puertos, pero no el protocolo
        return self.port_specified_but_not_protocol(
            is_source=True
        ) or self.port_specified_but_not_protocol(is_source=False)

    def port_specified_but_not_protocol(self, is_source):
        # Si se especifica uno de los puertos, pero no el protocolo
        if is_source:
            return self.blocked_src_port and not self.blocked_protocol
        return self.blocked_dst_port and not self.blocked_protocol

    def create_rules_between_any_hosts(self):
        # Si entro aca, por lo menos uno de los dos hosts no esta definido
        if self.any_port_specified_but_not_protocol():
            return self.create_rules_between_any_hosts_with_port()
        if self.blocked_protocol:
            return self.create_rules_between_any_hosts_with_protocol()
        return self.create_rules_between_any_hosts_with_no_port_and_no_protocol()

    def create_rules_between_any_hosts_with_port(self):
        # Protocolo no definido, aunque no este en el nombre del metodo
        rule_1 = {
            "dl_src": self.get_blocked_src_host_address(),
            "dl_dst": self.get_blocked_dst_host_address(),
            "dl_type": pkt.ethernet.IP_TYPE,
            "tp_src": self.blocked_src_port,
            "tp_dst": self.blocked_dst_port,
            "nw_proto": pkt.ipv4.UDP_PROTOCOL,
        }
        rule_2 = {
            "dl_src": self.get_blocked_src_host_address(),
            "dl_dst": self.get_blocked_dst_host_address(),
            "dl_type": pkt.ethernet.IP_TYPE,
            "tp_src": self.blocked_src_port,
            "tp_dst": self.blocked_dst_port,
            "nw_proto": pkt.ipv4.TCP_PROTOCOL,
        }
        return [rule_1, rule_2]

    def create_rules_between_any_hosts_with_protocol(self):
        # Protocolo definido, los otros parametros pueden o no estar definidos
        rule_1 = {
            "dl_src": self.get_blocked_src_host_address(),
            "dl_dst": self.get_blocked_dst_host_address(),
            "dl_type": pkt.ethernet.IP_TYPE,
            "tp_src": self.blocked_src_port,
            "tp_dst": self.blocked_dst_port,
            "nw_proto": self.blocked_protocol,
        }
        return [rule_1]

    def create_rules_between_any_hosts_with_no_port_and_no_protocol(self):
        # Solamente uno de los puertos deberia estar definido
        rule_1 = {
            "dl_src": self.get_blocked_src_host_address(),
            "dl_dst": self.get_blocked_dst_host_address(),
            "dl_type": pkt.ethernet.IP_TYPE,
            "tp_dst": None,
            "nw_proto": None,
        }
        return [rule_1]
