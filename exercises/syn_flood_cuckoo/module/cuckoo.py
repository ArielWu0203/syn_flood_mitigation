from module.global_variable import server_ip
from module.hash_function import *

def cuckoo2_method(n, m, r, s, file_name):
    T=5
    """Make a map bwtween ip and MAC
    """
    ip_map_MAC=dict()
    MAC_file=open("./MAC_address/MAC_address_%d"%(m+n), 'r')
    for i in range(2, 2+m+n):
        ip_map_MAC["10.0.2.%d"%i]=MAC_file.readline().strip()
    
    suspect_mac=set()
    malicious_mac=set()
    normal_mac=set()
    for i in range(2, 2+m):
        malicious_mac.add(ip_map_MAC["10.0.2.%d"%i])
    for i in range(2+m, 2+m+n):
        normal_mac.add(ip_map_MAC["10.0.2.%d"%i])

    """Read packet file and construct cuckoo filter
    """
    column=4
    row=int(s/column)
    lst = [{'ip':'', 'mac':'', 'counter':0} for i in range(s)]
    packet_file=open(file_name, 'r')
    packet_lines=packet_file.readlines()
    for packet in packet_lines:
        (timestamp, flag, src_ip, dst_ip) = [t(s) for t,s in zip((float,str, str, str),packet.split())]
        key=["",""]
        if(flag=="SA"):
            key[0]=src_ip
            key[1]=ip_map_MAC[dst_ip]
        elif(flag=="A" and src_ip not in server_ip):
            key[0]=dst_ip
            key[1]=ip_map_MAC[src_ip]
        else:
            continue
        # Check if the ip exists in suspect_ip set
        # if key[1] in suspect_mac:
        #     continue
        hash_result=hash_ip_mac(key[0], key[1])
        index_1=hash_result%row
        index_2=(hash_result+17)%row
        """ Check if the key exits and empty slots
        """
        if(flag=="SA"):
            empty_slot_flag=False
            empty_slot_index=0
            find_slot=False
            for c in range(0, column):
                index=index_1*column+c
                if(empty_slot_flag is False and lst[index]['counter']==0):
                    empty_slot_flag=True
                    empty_slot_index=index
                elif(lst[index]['ip']==key[0] and lst[index]['mac']==key[1]):
                    lst[index]['counter']+=1
                    find_slot=True
                    """Check if the counter surpass threshold
                    """
                    if(lst[index]['counter']>T):
                        suspect_mac.add(lst[index]['mac'])
                        lst[index]['ip']=''
                        lst[index]['mac']=''
                        lst[index]['counter']=0
                    break
                index=index_2*column+c
                if(empty_slot_flag is False and lst[index]['counter']==0):
                    empty_slot_flag=True
                    empty_slot_index=index
                elif(lst[index]['ip']==key[0] and lst[index]['mac']==key[1]):
                    lst[index]['counter']+=1
                    find_slot=True
                    if(lst[index]['counter']>T):
                        """Check if the counter surpass threshold
                        """
                        suspect_mac.add(lst[index]['mac'])
                        lst[index]['ip']=''
                        lst[index]['mac']=''
                        lst[index]['counter']=0
                    break
            if(find_slot is False and empty_slot_flag is True):
                lst[empty_slot_index]['ip']=key[0]
                lst[empty_slot_index]['mac']=key[1]
                lst[empty_slot_index]['counter']=1

        elif(flag=="A" and src_ip not in server_ip):
            for c in range(0, column):
                index=index_1*column+c
                if(lst[index]['ip']==key[0] and lst[index]['mac']==key[1]):
                    lst[index]['ip']=''
                    lst[index]['mac']=''
                    lst[index]['counter']=0
                    break
                index=index_2*column+c
                if(lst[index]['ip']==key[0] and lst[index]['mac']==key[1]):
                    lst[index]['ip']=''
                    lst[index]['mac']=''
                    lst[index]['counter']=0
                    break
    specificity = (n-len(normal_mac&suspect_mac))/n
    precision = len(malicious_mac&suspect_mac)/m
    accuracy=((n-len(normal_mac&suspect_mac))+len(malicious_mac&suspect_mac))/(n+m)
    return (specificity, precision, accuracy)
