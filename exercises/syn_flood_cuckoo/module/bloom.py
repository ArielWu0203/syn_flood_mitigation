from module.global_variable import *
from module.hash_function import *

MAX=65535
misjudged_normal_ip=set()

def bloom_method(n, m, r, e, file_name, T):
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
                """Checking
                """
                # check_normal_ip(src_ip, normal_ip, malicious_ip, index_map_ip, syn_bloom, other_bloom, e)
            # Decrease the number
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
    # print("有重疊到的index")
    # for i in range(0, e):
    #     if(len(index_map_ip[i])>1):
    #         print("index: %d syn_count: %d other_count: %d" % (i, syn_bloom[i], other_bloom[i]))
    #         print("normal ip count: %d" % len(index_map_ip[i] & normal_ip))
    #         print("malicious ip count: %d" % len(index_map_ip[i] & malicious_ip))
    # check_all(suspect_ip, normal_ip, malicious_ip, index_map_ip, syn_bloom, other_bloom, e, T)
    # print("沒有被判斷到的攻擊者ip -- 數量: %d" % len(malicious_ip-suspect_ip))
    # print(malicious_ip-suspect_ip)
    return (specificity, precision, accuracy)

def check_normal_ip(ip, normal_ip, malicious_ip, index_map_ip, syn_bloom, other_bloom, e):
    if(ip not in normal_ip or ip in misjudged_normal_ip):
        return
    else: # 誤判正常者
        misjudged_normal_ip.add(ip)
        print("誤判的正常者 %s" % ip)
        syn_min=MAX
        other_min=MAX
        own = set()
        own.add(ip)
        for i in range(0, e):
            if(ip in index_map_ip[i]):
                print("index: %d syn_count=%d other_count=%d" %(i, syn_bloom[i], other_bloom[i]))
                same_index_ip = index_map_ip[i] - own
                print("malicious ip count: %d" % len(same_index_ip&malicious_ip))
                print("normal ip count: %d" % len(same_index_ip&normal_ip))
        print("----------\n")

def check_all(suspect_ip, normal_ip, malicious_ip, index_map_ip, syn_bloom, other_bloom, e, T):
    # 看沒有被誤判的正常者的 hash 狀況
    correctjudged_normal_ip=normal_ip-suspect_ip
    for ip in correctjudged_normal_ip:
        print("沒有被誤判的正常者 %s" % ip)
        syn_min=MAX
        other_min=MAX
        own = set()
        own.add(ip)
        for i in range(0, e):
            if(ip in index_map_ip[i]):
                print("index: %d syn_count=%d other_count=%d" %(i, syn_bloom[i], other_bloom[i]))
                same_index_ip = index_map_ip[i] - own
                print("malicious ip count: %d" % len(same_index_ip&malicious_ip))
                print("normal ip count: %d" % len(same_index_ip&normal_ip))
        print("----------\n")
    # 少判斷到攻擊者
    # loss_malicious_ip = malicious_ip - suspect_ip
    # for ip in loss_malicious_ip:

        