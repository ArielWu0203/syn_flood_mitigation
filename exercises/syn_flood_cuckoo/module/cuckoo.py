from module.global_variable import server_ip
from module.hash_function import *

def cuckoo2_method(n, m, r, s, file_name, MAC_file):
    T=5
    """Make a map bwtween ip and MAC
    """
    ip_map_MAC=dict()
    MAC_file=open(MAC_file, 'r')
    for i in range(2, 2+m+n):
        ip_map_MAC["10.0.2.%d"%i]=MAC_file.readline().strip()
    
    suspect_mac=set()
    white_mac=set()
    hash_in_table_mac=set()
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
        if(timestamp>120):
            break
        key=["",""]
        if(flag=="SA"):
            key[0]=src_ip
            key[1]=ip_map_MAC[dst_ip]
        elif(flag=="A" and src_ip not in server_ip):
            key[0]=dst_ip
            key[1]=ip_map_MAC[src_ip]
        else:
            continue
        # Check if the mac exists in suspect_mac set and the mac exists in white_mac set
        if (key[1] in suspect_mac or key[1] in white_mac) :
            continue
        hash_result=hash_ip_mac(key[0], key[1])
        index_1=hash_result%row
        index_2=(hash_result+59)%row
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
                hash_in_table_mac.add(key[1])

        elif(flag=="A" and src_ip not in server_ip):
            for c in range(0, column):
                index=index_1*column+c
                if(lst[index]['ip']==key[0] and lst[index]['mac']==key[1]):
                    lst[index]['ip']=''
                    lst[index]['mac']=''
                    lst[index]['counter']=0
                    white_mac.add(lst[index]['mac'])
                    break
                index=index_2*column+c
                if(lst[index]['ip']==key[0] and lst[index]['mac']==key[1]):
                    lst[index]['ip']=''
                    lst[index]['mac']=''
                    lst[index]['counter']=0
                    white_mac.add(lst[index]['mac'])
                    break
    # 漏抓到的攻擊者的原因
    attcker_count_not_exceed_threshold = set()
    for item in lst:
        uncatched_attacket_mac =  malicious_mac-suspect_mac
        if item['mac'] in uncatched_attacket_mac:
            if(item['counter']<=T):
                attcker_count_not_exceed_threshold.add(item['mac'])
            # print("mac: %s count: %d" %(item['mac'], item['counter']))
    specificity = (n-len(normal_mac&suspect_mac))/n
    precision = len(malicious_mac&suspect_mac)/m
    accuracy=((n-len(normal_mac&suspect_mac))+len(malicious_mac&suspect_mac))/(n+m)
    test_2=False
    if(uncatched_attacket_mac == attcker_count_not_exceed_threshold):
        test_2=True
    return (specificity, precision, accuracy, test_2)
