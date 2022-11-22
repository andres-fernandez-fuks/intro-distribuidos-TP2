import pox.lib.packet as pkt
from block_rule import (
    GenericBlockRule,
    BlockRuleTypeI,
    BlockRuleTypeII,
    BlockRuleTypeIII,
)

# Esta variable indica que switch aplicara el firewall
FIREWALL_SWITCH_ID = 1

# Definiciones de las reglas por defecto, con sus campos respectivos

rule_1_restrictions = {
    "dst_port": 80,
}

rule_2_restrictions = {
    "src_host": 1,
    "dst_port": 5001,
    "protocol": pkt.ipv4.UDP_PROTOCOL,
}

rule_3_restrictions = {
    "src_host": 2,  # No importa cual es src y cual es dst
    "dst_host": 4,
}

# Reglas extra

extra_rule_restrictions = {
    "src_host": 1,
    "dst_host": 2,
    "src_port": 5001,
    "dst_port": 8001,
}

extra_rule = GenericBlockRule(extra_rule_restrictions)

ACTIVE_RULES = [
    BlockRuleTypeI(),
    BlockRuleTypeII(),
    BlockRuleTypeIII(),
    # extra_rule,
]
