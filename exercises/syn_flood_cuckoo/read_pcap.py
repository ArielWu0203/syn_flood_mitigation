import click
from scapy.all import *

"""Input format
1. n : # of users
2. m : # of attackers
3. r : the rate of attack
"""
"""Output format
1. timestamp
2. tcp_flags
3. src_ip
4. dst_ip
"""
def read_pcap(n, m, r):
    f = "./testing/n%d_m%d_r%s.pcap"%(n, m, r)
    print(f)
    packets = rdpcap(f)
    first_time = packets[0].time
    with open("./analysis/n%d_m%d_r%s.txt"%(n, m, r), 'w') as f:
        for packet in packets:
            if packet.haslayer(TCP):
                f.write("%f %s %s %s\n" % (packet.time-first_time, packet[TCP].flags, packet[IP].src, packet[IP].dst))
