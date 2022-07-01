import click
from read_pcap import read_pcap 
import numpy as np
import os.path
from module.global_variable import *
from module.hash_function import *
from module.bloom import bloom_method
from module.cuckoo import cuckoo2_method

"""Input format
1. sc: which scenario
2. n : # of users 後 n 個 ip 都是攻擊者
3. m : # of attackers 前 m 個 ip 都是攻擊者
4. r : the rate of attack
5. e : # of entries for bloom filter
6. s : # of slots for cuckoo
"""
@click.command()
@click.option('-sc',help='scenario', type=click.INT)
@click.option('-n', help='# of nomral users', type=click.INT)
@click.option('-m', help='# of attackers', type=click.INT)
@click.option('-r', help='rate of attack')
@click.option('-e', help='# of entries for bloom filter', type=click.INT)
@click.option('-s', help='# of slots for cuckoo', type=click.INT)
def call_method( sc, n, m, r, e, s):
    if(sc == 1):
        scenario_1(n, m, r, e)
    elif(sc == 2):
        scenario_2(n, e, s)
    elif(sc == 3):
        scenario_3(n, e, s)
    elif(sc==5):
        scenario_5(m, e, s)
    elif(sc==100):
        test(n, m, r, e, s)

def test(n, m, r, e, s):
    analysis_file = "./analysis/n%d_m%d_r%s.txt"%(n, m, r)
    (specificity, precision, accuracy) = bloom_method(n, m, r, e, analysis_file, threshold)
    print(specificity, precision, accuracy) 

"""Input format
1. n : # of users
2. m : # of attackers
3. r: attack rate
4. e : the number of entries
5. input file name
"""
def scenario_1(n, m, r, e):
    analysis_file = "./analysis/n%d_m%d_r%s.txt"%(n, m, r)
    if not os.path.isfile(analysis_file):
        read_pcap(n, m, r)
    output_file=open("./bloom_plot/n%d_m%d_r%s.txt"%(n, m, r), 'w')
    for T in np.arange(0.1, 2.1, 0.1):
        (specificity, precision, accuracy) = bloom_method(n,m,r,e,analysis_file,T)
        output_file.write("%f %f %f %f\n"% (T, specificity, precision, accuracy))
            

"""Input format
1. n : # of users
2. m : # of attackers
3. e : # of entries for bloom
4. s : # of slots for cuckoo
5. input file name
"""
def scenario_2(n, e, s):
    rate = "u200000"
    output_file_bloom=open("./plot_dataset/bloom/n%d_r%s_s2.txt"%(n, rate), 'w')
    output_file_cuckoo_2=open("./plot_dataset/cuckoo2/n%d_r%s_s2.txt"%(n, rate), 'w')
    for attacker_num in  range(20, 81, 10):
        analysis_file = "./analysis/n%d_m%d_r%s.txt"%(n, attacker_num, rate)
        if not os.path.isfile(analysis_file):
            read_pcap(n, attacker_num, rate)
        (specificity, precision, accuracy) = cuckoo2_method(n, attacker_num, rate, s, analysis_file)
        output_file_cuckoo_2.write("%d %f %f %f\n"% (attacker_num, specificity, precision, accuracy))
        (specificity, precision, accuracy) = bloom_method(n, attacker_num, rate, e, analysis_file, threshold)
        output_file_bloom.write("%d %f %f %f\n"% (attacker_num, specificity, precision, accuracy))

"""Input format
1. n : # of users
2. m : # of attackers
3. e : # of entries for bloom
4. s : # of slots for cuckoo
5. input file name
"""
def scenario_3(n, e, s):
    rate = "4"
    output_file_bloom=open("./plot_dataset/bloom/n%d_r%s_s3.txt"%(n, rate), 'w')
    output_file_cuckoo_2=open("./plot_dataset/cuckoo2/n%d_r%s_s3.txt"%(n, rate), 'w')
    for attacker_num in  range(20, 81, 10):
        analysis_file = "./analysis/n%d_m%d_r%s.txt"%(n, attacker_num, rate)
        read_pcap(n, attacker_num, rate)
        (specificity, precision, accuracy) = cuckoo2_method(n, attacker_num, rate, s, analysis_file)
        output_file_cuckoo_2.write("%d %f %f %f\n"% (attacker_num, specificity, precision, accuracy))
        (specificity, precision, accuracy) = bloom_method(n, attacker_num, rate, e, analysis_file, threshold)
        output_file_bloom.write("%d %f %f %f\n"% (attacker_num, specificity, precision, accuracy))

def scenario_5(m, e, s):
    rate = "u200000"
    output_file_bloom=open("./plot_dataset/bloom/m%d_r%s_s5.txt"%(m, rate), 'w')
    output_file_cuckoo_2=open("./plot_dataset/cuckoo2/m%d_r%s_s5.txt"%(m, rate), 'w')
    for normal_num in range(10, 41, 5):
        analysis_file = "./analysis/n%d_m%d_r%s.txt"%(normal_num, m, rate)
        if not os.path.isfile(analysis_file):
            read_pcap(normal_num, m, rate)
        (specificity, precision, accuracy) = cuckoo2_method(normal_num, m, rate, s, analysis_file)
        output_file_cuckoo_2.write("%d %f %f %f\n"% (normal_num, specificity, precision, accuracy))
        (specificity, precision, accuracy) = bloom_method(normal_num, m, rate, e, analysis_file, threshold)
        output_file_bloom.write("%d %f %f %f\n"% (normal_num, specificity, precision, accuracy))

if __name__ == '__main__':
    call_method()