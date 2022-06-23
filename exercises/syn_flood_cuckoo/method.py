import click
from read_pcap import read_pcap 
import numpy as np
import binascii
import os.path

MAX=65535
server_ip="10.0.1.1"
def hash_ip(src_ip, dst_ip):
    ipbytes=bytes(map(int, src_ip.split('.')))+bytes(map(int, dst_ip.split('.')))
    hash_result = binascii.crc32(ipbytes)
    return hash_result

"""Input format
1. method: choose which method
2. n : # of users 後 n 個 ip 都是攻擊者
3. m : # of attackers 前 m 個 ip 都是攻擊者
4. r : the rate of attack
"""
@click.command()
@click.option('--method',type=click.Choice(['bloom', 'cuckoo_1', 'cuckoo_2'], case_sensitive=False))
@click.option('-n', help='# of nomral users', type=click.INT)
@click.option('-m', help='# of attackers', type=click.INT)
@click.option('-r', help='rate of attack')
@click.option('-e', help='# of entries for bloom filter', type=click.INT)
def call_method(method, n, m, r, e):
    analysis_file = "./analysis/n%d_m%d_r%s.txt"%(n, m, r)
    if not os.path.isfile(analysis_file):
        read_pcap(n, m, r)
    if(method == 'bloom'):
        bloom_method(n, m, r, e, analysis_file)

"""Input format
1. n : # of users
2. m : # of attackers
3. e : the number of entries
"""
def bloom_method(n, m, r, e, file_name):
    with open(file_name, 'r') as f:
        all_lines=f.readlines()
        malicious_ip = set()
        normal_ip=set()
        for i in range(2, 2+m):
            malicious_ip.add("10.0.2.%d"%i)
        for i in range(2+m, 2+m+n):
            normal_ip.add("10.0.2.%d"%i)
        # print("T \t specificity \t precision")
        # print("= \t =========== \t =========")
        """Open the file
        """
        output_file=open("./bloom_plot/n%d_m%d_r%s.txt"%(n, m, r), 'w')
        for T in np.arange(0.00001, 0.00021, 0.00001):
            suspect_ip=set()
            syn_bloom=[0]*e
            other_bloom=[0]*e
            counter=0
            counter_max=100
            for line in all_lines:
                (timestamp, flag, src_ip, dst_ip) = [t(s) for t,s in zip((float,str, str, str),line.split())]
                if(timestamp>30.0):
                    break
                elif(dst_ip == server_ip):
                    # hash index
                    h=[0]*4
                    h[0]=hash_ip(src_ip, dst_ip)%e
                    h[1]=(hash_ip(src_ip, dst_ip)+17)%e
                    h[2]=(hash_ip(src_ip, dst_ip)+19)%e
                    h[3]=(hash_ip(src_ip, dst_ip)+23)%e
                    syn_min=MAX
                    other_min=MAX
                    if(flag=="S"):
                        for x in h:
                            syn_bloom[x]+=1
                            if(syn_bloom[x]<syn_min):
                                syn_min=syn_bloom[x]
                    else:
                        for x in h:
                            other_bloom[x]+=1
                            if(other_bloom[x]<other_min):
                                other_min=other_bloom[x]
                    # Check the threshold
                    if(other_min>=30 and syn_min/other_min>T):
                        suspect_ip.add(src_ip)
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
            output_file.write("%f %f %f\n"% (T, specificity, precision))
            

# def cuckoo_1_method():

# def cuckoo_2_method():

if __name__ == '__main__':
    call_method()