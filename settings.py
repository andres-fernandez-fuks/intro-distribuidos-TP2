import pox.lib.packet as pkt
import block_rule as br

# Esta variable indica que switchs aplicaran el firewall
FIREWALL_SWITCH_ID = 1

# Variables referidas a reglas solicitadas
R1_BLOCKED_DST_PORT = 80
R2_BLOCKED_SRC_ADDR = 1
R2_BLOCKED_DST_PORT = 5001
R2_BLOCKED_PROTOCOL = pkt.ipv4.UDP_PROTOCOL
R3_BLOCKED_1_ADDR = 2
R3_BLOCKED_2_ADDR = 4

rule_1_restrictions = {
    "dst_port": R1_BLOCKED_DST_PORT,
}

rule_2_restrictions = {
    "src_host": R2_BLOCKED_SRC_ADDR,
    "dst_port": R2_BLOCKED_DST_PORT,
    "protocol": R2_BLOCKED_PROTOCOL,
}

rule_3_restrictions = {
    "src_host": R3_BLOCKED_1_ADDR,
    "dst_host": R3_BLOCKED_2_ADDR,
    "src_port": 80,  # no se usa como src_port, se usa como dst_host para el trafico que va de ADDR2 a ADDR1
    "dst_port": 5001,
    "protocol": pkt.ipv4.UDP_PROTOCOL,
}

ACTIVE_RULES = [
    br.GenericBlockRule(rule_1_restrictions),
    br.GenericBlockRule(rule_2_restrictions),
    # br.GenericBlockRule(rule_3_restrictions),
]
