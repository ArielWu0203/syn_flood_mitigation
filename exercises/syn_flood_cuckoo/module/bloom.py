from module.global_variable import *
from module.hash_function import *

MAX=65535
misjudged_normal_ip=set()

def bloom_method(n, m, r, e, file_name, T, use_decreasing):
    f=open(file_name, 'r')
    all_lines=f.readlines()
    malicious_ip = set()
    normal_ip=set()
    for i in range(2, 2+m):
        malicious_ip.add("10.0.2.%d"%i)
    for i in range(2+m, 2+m+n):
        normal_ip.add("10.0.2.%d"%i)
    """Open the file
    """
    suspect_ip=set()
    syn_bloom=[0]*e
    other_bloom=[0]*e
    counter=0
    counter_max=500

    """For checking
    """
    client_map_server=dict()
    index_map_ip = dict()
    for i in range(0, e):
        index_map_ip[i]=set()

    for line in all_lines:
        (timestamp, flag, src_ip, dst_ip) = [t(s) for t,s in zip((float,str, str, str),line.split())]
        if(timestamp>120):
            break
        if(dst_ip in server_ip):
            """Hash index and increment the counter
            """
            h=[0]*4
            h[0]=hash_ip(src_ip, dst_ip)%e
            h[1]=(hash_ip(src_ip, dst_ip)+17)%e
            h[2]=(hash_ip(src_ip, dst_ip)+19)%e
            h[3]=(hash_ip(src_ip, dst_ip)+23)%e
            if(flag=="S"):
                for x in h:
                    syn_bloom[x]+=1
            else:
                for x in h:
                    other_bloom[x]+=1
            """Want to know every index'es ip
            """
            for x in h:
                index_map_ip[x].add(src_ip)
            """Add client map to server
            """
            client_map_server[src_ip]=dst_ip

            """Check the threshold
            step1: get the min of syn and other bloom
            step2: test the threshold
            """
            syn_min=MAX
            other_min=MAX
            syn_min_index=e
            other_min_index=e
            for x in h:
                if(syn_bloom[x]<syn_min):
                    syn_min=syn_bloom[x]
                    syn_min_index=x
                if(other_bloom[x]<other_min):
                    other_min=other_bloom[x]
                    other_min_index=x
            if(other_min>=10 and syn_min/other_min>T):
                suspect_ip.add(src_ip)
            if(use_decreasing is True):
                counter+=1
                if(counter>=counter_max):
                    counter=0
                    for i in range(0, e):
                        if(syn_bloom[i]>0):
                            syn_bloom[i]-=1
                        if(other_bloom[i]>0):
                            other_bloom[i]-=1
    specificity = (n-len(normal_ip&suspect_ip))/n
    precision = len(malicious_ip&suspect_ip)/m
    accuracy=((n-len(normal_ip&suspect_ip))+len(malicious_ip&suspect_ip))/(n+m)
    test_1=check_all_normal_ip(suspect_ip, normal_ip, malicious_ip, index_map_ip, syn_bloom, other_bloom, e, T)
    test_3=True
    if(use_decreasing is False):
        test_3=check_all_malicious_ip(suspect_ip, normal_ip, malicious_ip, index_map_ip, syn_bloom, other_bloom, e, T)
    return (specificity, precision, accuracy, test_1, test_3)

def check_all_normal_ip(suspect_ip, normal_ip, malicious_ip, index_map_ip, syn_bloom, other_bloom, e, T):
    misjudged_normal_ip = normal_ip & suspect_ip
    four_index_overlapping=set()

    for ip in misjudged_normal_ip:
        syn_min=MAX
        other_min=MAX
        own = set()
        own.add(ip)
        overlapping_index_count = 0
        # print("ip: %s" % ip)
        for i in range(0, e):
            if(ip in index_map_ip[i]):
                if(syn_min>syn_bloom[i]):
                    syn_min=syn_bloom[i]
                if(other_min>other_bloom[i]):
                    other_min=other_bloom[i]
                same_index_ip = index_map_ip[i] - own
                if(len(same_index_ip & malicious_ip)>0):
                    overlapping_index_count+=1
        #         print("index: %d syn_count: %d other_count: %d" % (i, syn_bloom[i], other_bloom[i]))
        #         print( same_index_ip)
        # print("syn count: %d other_count:%d" % (syn_min, other_min))
        # print("---------\n")
        if(overlapping_index_count==4):
            four_index_overlapping.add(ip)
    if(misjudged_normal_ip == four_index_overlapping):
        return True
    return False
        
def check_all_malicious_ip(suspect_ip, normal_ip, malicious_ip, index_map_ip, syn_bloom, other_bloom, e, T):
    # print("沒有被抓到的 attacker 數量")
    # print(len(malicious_ip-suspect_ip))
    for uncatched_attacker_ip in malicious_ip-suspect_ip:
        # print("ip: %s" %uncatched_attacker_ip)
        own=set()
        own.add(uncatched_attacker_ip)
        syn_min=MAX
        other_min=MAX
        overlapping_index_count = 0
        for index, ip_set in index_map_ip.items():
            if(uncatched_attacker_ip in ip_set):
                if(syn_min>syn_bloom[index]):
                    syn_min=syn_bloom[index]
                if(other_min>other_bloom[index]):
                    other_min=other_bloom[index]
                # print("index: %d 重疊的 ip 有" % index)
                # print(ip_set-own)
                if(len((ip_set-own) & normal_ip)>0):
                    overlapping_index_count+=1
        if(overlapping_index_count<4):
            return False
        # print("syn count: %d other count: %d" % (syn_min, other_min))
        # print("---------\n")
    return True
        