#!/usr/bin/env python3
import argparse
import grpc
import os
import sys
from time import sleep
import nnpy
import struct

# Import P4Runtime lib from parent utils dir
# Probably there's a better way of doing this.
sys.path.append(
    os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 '../../utils/'))
import p4runtime_lib.bmv2
from p4runtime_lib.switch import ShutdownAllSwitchConnections
import p4runtime_lib.helper

SWITCH_TO_HOST_PORT = 1
SWITCH_TO_SWITCH_PORT = 2

def writeForwardRules(p4info_helper,ingress_sw, dst_eth_addr, port, dst_ip_addr):
    table_entry = p4info_helper.buildTableEntry(
        table_name="MyIngress.ipv4_lpm",
        match_fields={
            "hdr.ipv4.dstAddr": (dst_ip_addr,32)
        },
        action_name="MyIngress.ipv4_forward",
        action_params={
            "dstAddr": dst_eth_addr,
            "port": port
        })
    # write into ingress of target sw
    ingress_sw.WriteTableEntry(table_entry)


def writeDropRules(p4info_helper, ingress_sw, src_ip_addr):
    table_entry = p4info_helper.buildTableEntry(
        table_name="MyIngress.black_list",
        match_fields={
            "hdr.ipv4.srcAddr": (src_ip_addr, 32)
        },
        action_name="MyIngress.drop",
        action_params={})
    ingress_sw.WriteTableEntry(table_entry)
    print("Installed ingress tunnel rule on %s" % ingress_sw.name)


def readTableRules(p4info_helper, sw):
    """
    Reads the table entries from all tables on the switch.

    :param p4info_helper: the P4Info helper
    :param sw: the switch connection
    """
    print('\n----- Reading tables rules for %s -----' % sw.name)
    for response in sw.ReadTableEntries():
        for entity in response.entities:
            entry = entity.table_entry
            # TODO For extra credit, you can use the p4info_helper to translate
            #      the IDs in the entry to names
            table_name = p4info_helper.get_tables_name(entry.table_id)
            print('%s: ' % table_name, end=' ')
            for m in entry.match:
                print(p4info_helper.get_match_field_name(table_name, m.field_id), end=' ')
                print('%r' % (p4info_helper.get_match_field_value(m),), end=' ')
            action = entry.action.action
            action_name = p4info_helper.get_actions_name(action.action_id)
            print('->', action_name, end=' ')
            for p in action.params:
                print(p4info_helper.get_action_param_name(action_name, p.param_id), end=' ')
                print('%r' % p.value, end=' ')
            print()

def SendDigestEntry(p4info_helper, sw, digest_name=None):
    digest_entry = p4info_helper.buildDigestEntry(digest_name=digest_name)
    sw.WriteDigestEntry(digest_entry)
    print(digest_entry)
    print("Sent DigestEntry via P4Runtime.")


def printGrpcError(e):
    print("gRPC Error:", e.details(), end=' ')
    status_code = e.code()
    print("(%s)" % status_code.name, end=' ')
    traceback = sys.exc_info()[2]
    print("[%s:%d]" % (traceback.tb_frame.f_code.co_filename, traceback.tb_lineno))

def main(p4info_file_path, bmv2_file_path):
    # Instantiate a P4Runtime helper from the p4info file
    p4info_helper = p4runtime_lib.helper.P4InfoHelper(p4info_file_path)

    try:
        # Create a switch connection object for s1 and s2;
        # this is backed by a P4Runtime gRPC connection.
        # Also, dump all P4Runtime messages sent to switch to given txt files.
        s1 = p4runtime_lib.bmv2.Bmv2SwitchConnection(
            name='s1',
            address='127.0.0.1:50051',
            device_id=0,
            proto_dump_file='logs/s1-p4runtime-requests.txt')

        # Send master arbitration update message to establish this controller as
        # master (required by P4Runtime before performing any other write operation)
        s1.MasterArbitrationUpdate()

        # Install the P4 program on the switches
        s1.SetForwardingPipelineConfig(p4info=p4info_helper.p4info,
                                       bmv2_json_file_path=bmv2_file_path)
        print("Installed P4 Program using SetForwardingPipelineConfig on s1")

        SendDigestEntry(p4info_helper, sw=s1, digest_name="black_list_digest")

        # Write the forwarding table
        writeForwardRules(p4info_helper,ingress_sw=s1, dst_eth_addr='08:00:00:00:01:11',port=1,dst_ip_addr='10.0.1.1')
        writeForwardRules(p4info_helper,ingress_sw=s1, dst_eth_addr='08:00:00:00:01:22',port=2,dst_ip_addr='10.0.1.2')
        writeForwardRules(p4info_helper,ingress_sw=s1, dst_eth_addr='08:00:00:00:01:33',port=2,dst_ip_addr='10.0.1.3')
        MAC_file = open('./MAC_address/MAC_address_15', 'r')
        i=2
        for mac_address in MAC_file.readlines():
            mac_address=mac_address.strip()
            ip_address='10.0.2.%d'%i
            writeForwardRules(p4info_helper,ingress_sw=s1, dst_eth_addr=mac_address,port=i+2,dst_ip_addr=ip_address)
            i+=1
        # Write the drop rules 
        # writeDropRules(p4info_helper, ingress_sw=s1, src_ip_addr='10.0.2.2')

        # TODO Uncomment the following two lines to read table entries from s1
        readTableRules(p4info_helper, s1)

        # print("Listening on socket")
        # sub = nnpy.Socket(nnpy.AF_SP, nnpy.SUB)
        # sub.connect('ipc:///tmp/bm-0-log.ipc')
        # sub.setsockopt(nnpy.SUB, nnpy.SUB_SUBSCRIBE, '')

        while True:
            digests = s1.DigestList()
            # msg = sub.recv()
            # (topic, device_id, ctx_id, list_id, buffer_id, num) = struct.unpack("<iQiiQi", msg[:32]) # nanomsg 的 control header
            # print((topic, device_id, ctx_id, list_id, buffer_id, num))
            # digest = self.unpack_digest(msg, num) # 解析 digest 的 payload

            # 发送 ACK 告诉交换机已经收到了信息
            # self.controller.client.bm_learning_ack_buffer(ctx_id, list_id, buffer_id)
            # print("message recieved")

    except KeyboardInterrupt:
        print(" Shutting down.")
    except grpc.RpcError as e:
        printGrpcError(e)

    ShutdownAllSwitchConnections()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='P4Runtime Controller')
    parser.add_argument('--p4info', help='p4info proto in text format from p4c',
                        type=str, action="store", required=False,
                        default='./build/basic.p4.p4info.txt')
    parser.add_argument('--bmv2-json', help='BMv2 JSON file from p4c',
                        type=str, action="store", required=False,
                        default='./build/basic.json')
    args = parser.parse_args()

    if not os.path.exists(args.p4info):
        parser.print_help()
        print("\np4info file not found: %s\nHave you run 'make'?" % args.p4info)
        parser.exit(1)
    if not os.path.exists(args.bmv2_json):
        parser.print_help()
        print("\nBMv2 JSON file not found: %s\nHave you run 'make'?" % args.bmv2_json)
        parser.exit(1)
    main(args.p4info, args.bmv2_json)
