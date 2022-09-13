import random
import click
import json 

@click.command()
@click.option('-n', help='the number of normal users and attacker', type=click.INT)
def output_topofile(n):
    make_topo(n)
    make_s1(n)

def make_s1(n):
    dict = {
        "target": "bmv2",
        "p4info": "build/basic.p4.p4info.txt",
        "bmv2_json": "build/basic.json",
        "table_entries": [
            {
                "table": "MyIngress.ipv4_lpm",
                "default_action": True,
                "action_name": "MyIngress.drop",
                "action_params": { }
            },
            {
                "table": "MyIngress.ipv4_lpm",
                "match": {
                    "hdr.ipv4.dstAddr": ["10.0.1.1", 32]
                },
                "action_name": "MyIngress.ipv4_forward",
                "action_params": {
                    "dstAddr": "08:00:00:00:01:11",
                    "port": 1
                }
            },
            {
                "table": "MyIngress.ipv4_lpm",
                "match": {
                    "hdr.ipv4.dstAddr": ["10.0.1.2", 32]
                },
                "action_name": "MyIngress.ipv4_forward",
                "action_params": {
                    "dstAddr": "08:00:00:00:01:22",
                    "port": 2
                }
            },
            {
                "table": "MyIngress.ipv4_lpm",
                "match": {
                    "hdr.ipv4.dstAddr": ["10.0.1.3", 32]
                },
                "action_name": "MyIngress.ipv4_forward",
                "action_params": {
                    "dstAddr": "08:00:00:00:01:33",
                    "port": 3
                }
            }
        ]
    }


    with open("./MAC_address/MAC_address_"+str(n)) as f:
        i=2
        while True:
            mac = f.readline().strip()
            if(mac == ''):
                break
            object={
                "table": "MyIngress.ipv4_lpm",
                "match": {
                    "hdr.ipv4.dstAddr": ["10.0.2.%d"%i, 32]
                },
                "action_name": "MyIngress.ipv4_forward",
                "action_params": {
                    "dstAddr": mac,
                    "port": i+2
                }
            }
            dict["table_entries"].append(object)
            i+=1

    with open("./hosts-topo/s1-runtime.json", "w") as outfile:
        json.dump(dict, outfile, indent=4)

def make_topo(n):
    dict = {
        "hosts": {
            "h1": {"ip": "10.0.1.1/24", "mac": "08:00:00:00:01:11",
                "commands":["route add default gw 10.0.1.254 dev eth0",
                        "arp -i eth0 -s 10.0.1.254 08:00:00:00:01:00",
                        "python3 -m http.server 80 &"]},
            "h2": {"ip": "10.0.1.2/24", "mac": "08:00:00:00:01:22",
                "commands":["route add default gw 10.0.1.254 dev eth0",
                        "arp -i eth0 -s 10.0.1.254 08:00:00:00:01:00",
                        "python3 -m http.server 80 &"]},
            "h3": {"ip": "10.0.1.3/24", "mac": "08:00:00:00:01:33",
                "commands":["route add default gw 10.0.1.254 dev eth0",
                        "arp -i eth0 -s 10.0.1.254 08:00:00:00:01:00",
                        "python3 -m http.server 80 &"]}
        },
        "switches": {
            "s1": { "runtime_json" : "hosts-topo/s1-runtime.json" }
        },
        "links": [
            ["h1", "s1-p1"], ["h2", "s1-p2"], ["h3", "s1-p3"]
        ]
    }

    with open("./MAC_address/MAC_address_"+str(n)) as f:
        i=2
        while True:
            mac = f.readline().strip()
            if(mac == ''):
                break
            dict["hosts"]["h"+str(i+2)] = {
                "ip": "10.0.2.%d/24" % i, "mac": mac,
                "commands":[
                    "route add default gw 10.0.2.254 dev eth0",
                    "arp -i eth0 -s 10.0.2.254 08:00:00:00:01:00"
                ]
            }
            dict["links"].append(["h%d"%(i+2), "s1-p%d"%(i+2)])
            i+=1

    with open("./hosts-topo/topology.json", "w") as outfile:
        json.dump(dict, outfile, indent=4)

if __name__ == '__main__':
    output_topofile()