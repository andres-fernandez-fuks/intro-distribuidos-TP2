import pox.lib.packet as pkt

# Esta variable indica que switchs aplicaran el firewall
FIREWALL_SWITCH_ID = 1

# Variables referidas a reglas solicitadas
R1_BLOCKED_DST_PORT = 80
R2_BLOCKED_SRC_ADDR = 1
R2_BLOCKED_DST_PORT = 5001
R2_BLOCKED_PROTOCOL = pkt.ipv4.UDP_PROTOCOL
R3_BLOCKED_1_ADDR = 2
R3_BLOCKED_2_ADDR = 4
