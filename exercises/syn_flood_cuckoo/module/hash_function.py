import binascii

def hash_ip(src_ip, dst_ip):
    ipbytes=bytes(map(int, src_ip.split('.')))+bytes(map(int, dst_ip.split('.')))
    hash_result = binascii.crc32(ipbytes)
    return hash_result

def hash_ip_mac(ip, mac):
    ip_mac_bytes=bytes(map(int, ip.split('.')))+binascii.unhexlify(mac.replace(':', ''))
    hash_result = binascii.crc32(ip_mac_bytes)
    return hash_result