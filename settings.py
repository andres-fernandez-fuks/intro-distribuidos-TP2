import pox.lib.packet as pkt
from block_rule import (
    GenericBlockRule,
    BlockRuleTypeI,
    BlockRuleTypeII,
    BlockRuleTypeIII,
)

# Esta variable indica que switch aplicara el firewall
FIREWALL_SWITCH_ID = 4

# Variables referidas a reglas por defecto
R1_BLOCKED_DST_PORT = 80
R2_BLOCKED_SRC_ADDR = 1
R2_BLOCKED_DST_PORT = 5001
R2_BLOCKED_PROTOCOL = pkt.ipv4.UDP_PROTOCOL
R3_BLOCKED_1_ADDR = 2
R3_BLOCKED_2_ADDR = 4

# Definiciones de las reglas por defecto, con sus campos respectivos
rule_1_restrictions = {
    "dst_port": R1_BLOCKED_DST_PORT,
}

rule_2_restrictions = {
    "src_host": R2_BLOCKED_SRC_ADDR,
    "dst_port": R2_BLOCKED_DST_PORT,
    "protocol": R2_BLOCKED_PROTOCOL,
}

rule_3_restrictions = {
    "src_host": R3_BLOCKED_1_ADDR,  # No importa cual es src y cual es dst
    "dst_host": R3_BLOCKED_2_ADDR,
}

# Reglas extra
extra_rule_1 = {
    "dst_port": R1_BLOCKED_DST_PORT,
    "src_port": 81,
}  # funciona

extra_rule_2 = {
    "src_host": 1,
    "dst_port": 80,
    "src_port": 81,
    "protocol": pkt.ipv4.TCP_PROTOCOL,
}  # funciona

extra_rule_3 = {
    "src_host": R2_BLOCKED_SRC_ADDR,
    "dst_port": R2_BLOCKED_DST_PORT,
    "src_port": 8000,
    "protocol": R2_BLOCKED_PROTOCOL,
}

extra_rule_4 = {
    "src_host": R3_BLOCKED_1_ADDR,
    "dst_host": R3_BLOCKED_2_ADDR,
    "dst_port": 8001,
    "protocol": pkt.ipv4.ICMP_PROTOCOL,
}


ACTIVE_RULES = [
    # GenericBlockRule(extra_rule_4),
    BlockRuleTypeI()
    # BlockRuleTypeII(),
    # BlockRuleTypeIII(),
]
