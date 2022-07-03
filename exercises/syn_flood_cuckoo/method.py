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
@click.option('-d', help='output data directory will store in which directory')
def call_method( sc, n, m, r, e, s, d):
    if(sc == 1):
        scenario_1(n, m, r, e)
    elif(sc == 2):
        scenario_2(n, e, s, d)
    elif(sc == 3):
        scenario_3(n, e, s, d)
    elif(sc == 31): # test for none decreasing entry
        scenario_3_1(n, e, s, d)
    elif(sc == 4):
        scenario_4(n, e, s, d)
    elif(sc == 41): # test for none decreasing entry
        scenario_4_1(n, e, s, d)
    elif(sc==5):
        scenario_5(n, e, s, d)
    elif(sc==100):
        test_bloom(n, m, r, e, d)
    elif(sc==200):
        test_cuckoo(n, m, r, s, d)

def test_bloom(n, m, r, e, d):
    analysis_file = "./analysis/%s/n%d_m%d_r%s.txt"%(d, n, m, r)
    (specificity, precision, accuracy, test_1, test_3) = bloom_method(n, m, r, e, analysis_file, threshold, False)
    print(specificity, precision, accuracy, test_1, test_3) 

def test_cuckoo(n, m, r, s, d):
    analysis_file = "./analysis/%s/n%d_m%d_r%s.txt"%(d, n, m, r)
    MAC_file = "./MAC_address/%s/MAC_address_%d"%(d, m+n)
    (specificity, precision, accuracy, test_2) = cuckoo2_method(n, m, r, s, analysis_file, MAC_file)
    print(specificity, precision, accuracy, test_2)

"""Input format
1. n : # of users
2. m : # of attackers
3. r: attack rate
4. e : the number of entries
5. input file name
"""
def scenario_1(n, m, r, e, d):
    analysis_file = "./analysis/n%d_m%d_r%s.txt"%(n, m, r)
    if not os.path.isfile(analysis_file):
        read_pcap(n, m, r)
    output_file=open("./bloom_plot/n%d_m%d_r%s.txt"%(n, m, r), 'w')
    for T in np.arange(0.1, 2.1, 0.1):
        (specificity, precision, accuracy) = bloom_method(n,m,r,e,analysis_file,T)
        output_file.write("%f %f %f %f\n"% (T, specificity, precision, accuracy))
            

"""Input format
1. n : # of users
2. e : # of entries for bloom
3. s : # of slots for cuckoo
4. d: output data directory
"""
def scenario_2(n, e, s, d):
    rate = "u200000"
    output_file_bloom=open("./plot_dataset/bloom/%s/n%d_r%s_s2.txt"%(d, n, rate), 'w')
    output_file_cuckoo_2=open("./plot_dataset/cuckoo2/%s/n%d_r%s_s2.txt"%(d, n, rate), 'w')
    for attacker_num in  range(20, 81, 10):
        analysis_file = "./analysis/%s/n%d_m%d_r%s.txt"%(d, n, attacker_num, rate)
        MAC_file = "./MAC_address/%s/MAC_address_%d"%(d, attacker_num+n)
        if not os.path.isfile(analysis_file):
            read_pcap(n, attacker_num, rate, d)
        (specificity, precision, accuracy, test_2) = cuckoo2_method(n, attacker_num, rate, s, analysis_file, MAC_file)
        output_file_cuckoo_2.write("%d %f %f %f\n"% (attacker_num, specificity, precision, accuracy))
        (specificity, precision, accuracy, test_1, test_3) = bloom_method(n, attacker_num, rate, e, analysis_file, threshold, True)
        output_file_bloom.write("%d %f %f %f\n"% (attacker_num, specificity, precision, accuracy))
        if(test_1 is False):
            print('test _1 is false in %s/n%d_m%d_r%s.txt file' %(d, n, attacker_num, rate))
        if(test_2 is False):
            print('test _2 is false in %s/n%d_m%d_r%s.txt file' %(d, n, attacker_num, rate))


"""Input format
1. n : # of users
2. e : # of entries for bloom
3. s : # of slots for cuckoo
4. d: output data directory
"""
def scenario_3(n, e, s, d):
    rate = "4"
    output_file_bloom=open("./plot_dataset/bloom/%s/n%d_r%s_s3.txt"%(d, n, rate), 'w')
    output_file_cuckoo_2=open("./plot_dataset/cuckoo2/%s/n%d_r%s_s3.txt"%(d, n, rate), 'w')
    for attacker_num in  range(20, 81, 10):
        analysis_file = "./analysis/%s/n%d_m%d_r%s.txt"%(d, n, attacker_num, rate)
        MAC_file = "./MAC_address/%s/MAC_address_%d"%(d, attacker_num+n)
        if not os.path.isfile(analysis_file):
            read_pcap(n, attacker_num, rate, d)
        (specificity, precision, accuracy, test_2) = cuckoo2_method(n, attacker_num, rate, s, analysis_file, MAC_file)
        output_file_cuckoo_2.write("%d %f %f %f\n"% (attacker_num, specificity, precision, accuracy))
        (specificity, precision, accuracy, test_1, test_3) = bloom_method(n, attacker_num, rate, e, analysis_file, threshold, True)
        output_file_bloom.write("%d %f %f %f\n"% (attacker_num, specificity, precision, accuracy))
        if(test_1 is False):
            print('test _1 is false in %s/n%d_m%d_r%s.txt file' %(d, n, attacker_num, rate))
        if(test_2 is False):
            print('test _2 is false in %s/n%d_m%d_r%s.txt file' %(d, n, attacker_num, rate))
        if(test_3 is False):
            print('test _3 is false in %s/n%d_m%d_r%s.txt file' %(d, n, attacker_num, rate))

"""Input format
1. n : # of users
2. e : # of entries for bloom
3. s : # of slots for cuckoo
4. d: output data directory
"""
def scenario_3_1(n, e, s, d):
    rate = "4"
    output_file_bloom=open("./plot_dataset/bloom/%s/n%d_r%s_s3_1.txt"%(d, n, rate), 'w')
    output_file_bloom_none_T=open("./plot_dataset/bloom/%s/n%d_r%s_s3_1_none_T.txt"%(d, n, rate), 'w')
    output_file_cuckoo_2=open("./plot_dataset/cuckoo2/%s/n%d_r%s_s3_1.txt"%(d, n, rate), 'w')
    for attacker_num in  range(20, 81, 10):
        analysis_file = "./analysis/%s/n%d_m%d_r%s.txt"%(d, n, attacker_num, rate)
        MAC_file = "./MAC_address/%s/MAC_address_%d"%(d, attacker_num+n)
        if not os.path.isfile(analysis_file):
            read_pcap(n, attacker_num, rate, d)

        (specificity, precision, accuracy, test_2) = cuckoo2_method(n, attacker_num, rate, s, analysis_file, MAC_file)
        output_file_cuckoo_2.write("%d %f %f %f\n"% (attacker_num, specificity, precision, accuracy))
        if(test_2 is False):
            print('test _2 is false in %s/n%d_m%d_r%s.txt file' %(d, n, attacker_num, rate))

        (specificity, precision, accuracy, test_1, test_3) = bloom_method(n, attacker_num, rate, e, analysis_file, threshold, True)
        output_file_bloom.write("%d %f %f %f\n"% (attacker_num, specificity, precision, accuracy))
        if(test_1 is False):
            print('test _1 is false in %s/n%d_m%d_r%s.txt file' %(d, n, attacker_num, rate))
        if(test_3 is False):
            print('test _3 is false in %s/n%d_m%d_r%s.txt file' %(d, n, attacker_num, rate))
            
        (specificity, precision, accuracy, test_1, test_3) = bloom_method(n, attacker_num, rate, e, analysis_file, threshold, False)
        output_file_bloom_none_T.write("%d %f %f %f\n"% (attacker_num, specificity, precision, accuracy))
        if(test_1 is False):
            print('test _1 is false in %s/n%d_m%d_r%s.txt file' %(d, n, attacker_num, rate))
        if(test_3 is False):
            print('test _3 is false in %s/n%d_m%d_r%s.txt file' %(d, n, attacker_num, rate))
        

"""Input format
1. n : # of users
2. e : # of entries for bloom
3. s : # of slots for cuckoo
4. d: output data directory
"""
def scenario_4(n, e, s, d):
    rate = "1"
    output_file_bloom=open("./plot_dataset/bloom/%s/n%d_r%s_s4.txt"%(d, n, rate), 'w')
    output_file_cuckoo_2=open("./plot_dataset/cuckoo2/%s/n%d_r%s_s4.txt"%(d, n, rate), 'w')
    for attacker_num in  range(20, 81, 10):
        analysis_file = "./analysis/%s/n%d_m%d_r%s.txt"%(d, n, attacker_num, rate)
        MAC_file = "./MAC_address/%s/MAC_address_%d"%(d, attacker_num+n)
        if not os.path.isfile(analysis_file):
            read_pcap(n, attacker_num, rate, d)
        (specificity, precision, accuracy, test_2) = cuckoo2_method(n, attacker_num, rate, s, analysis_file, MAC_file)
        output_file_cuckoo_2.write("%d %f %f %f\n"% (attacker_num, specificity, precision, accuracy))
        if(test_2 is False):
            print('test _2 is false in %s/n%d_m%d_r%s.txt file' %(d, n, attacker_num, rate))
        (specificity, precision, accuracy, test_1, test_3) = bloom_method(n, attacker_num, rate, e, analysis_file, threshold, True)
        output_file_bloom.write("%d %f %f %f\n"% (attacker_num, specificity, precision, accuracy))
        if(test_1 is False):
            print('test _1 is false in %s/n%d_m%d_r%s.txt file' %(d, n, attacker_num, rate))

"""Input format
1. n : # of users
2. e : # of entries for bloom
3. s : # of slots for cuckoo
4. d: output data directory
"""
def scenario_4_1(n, e, s, d):
    rate = "1"
    output_file_bloom=open("./plot_dataset/bloom/%s/n%d_r%s_s4_1.txt"%(d, n, rate), 'w')
    output_file_bloom_none_T=open("./plot_dataset/bloom/%s/n%d_r%s_s4_1_none_T.txt"%(d, n, rate), 'w')
    output_file_cuckoo_2=open("./plot_dataset/cuckoo2/%s/n%d_r%s_s4_1.txt"%(d, n, rate), 'w')
    for attacker_num in  range(20, 81, 10):
        analysis_file = "./analysis/%s/n%d_m%d_r%s.txt"%(d, n, attacker_num, rate)
        MAC_file = "./MAC_address/%s/MAC_address_%d"%(d, attacker_num+n)
        if not os.path.isfile(analysis_file):
            read_pcap(n, attacker_num, rate, d)

        (specificity, precision, accuracy, test_2) = cuckoo2_method(n, attacker_num, rate, s, analysis_file, MAC_file)
        output_file_cuckoo_2.write("%d %f %f %f\n"% (attacker_num, specificity, precision, accuracy))
        if(test_2 is False):
            print('test _2 is false in %s/n%d_m%d_r%s.txt file' %(d, n, attacker_num, rate))

        (specificity, precision, accuracy, test_1, test_3) = bloom_method(n, attacker_num, rate, e, analysis_file, threshold, True)
        output_file_bloom.write("%d %f %f %f\n"% (attacker_num, specificity, precision, accuracy))
        if(test_1 is False):
            print('test _1 is false in %s/n%d_m%d_r%s.txt file' %(d, n, attacker_num, rate))
            
        (specificity, precision, accuracy, test_1, test_3) = bloom_method(n, attacker_num, rate, e, analysis_file, threshold, False)
        output_file_bloom_none_T.write("%d %f %f %f\n"% (attacker_num, specificity, precision, accuracy))
        if(test_1 is False):
            print('test _1 is false in %s/n%d_m%d_r%s.txt file' %(d, n, attacker_num, rate))
        if(test_3 is False):
            print('test _3 is false in %s/n%d_m%d_r%s.txt file' %(d, n, attacker_num, rate))


"""Input format
1. n : # of users
2. e : # of entries for bloom
3. s : # of slots for cuckoo
4. d: output data directory
"""
def scenario_5(n, e, s, d):
    rate = "1"
    output_file_bloom=open("./plot_dataset/bloom/%s/n%d_r%s_s5.txt"%(d, n, rate), 'w')
    output_file_cuckoo_2=open("./plot_dataset/cuckoo2/%s/n%d_r%s_s5.txt"%(d, n, rate), 'w')
    for attacker_num in  range(80, 81, 10):
        analysis_file = "./analysis/%s/n%d_m%d_r%s.txt"%(d, n, attacker_num, rate)
        MAC_file = "./MAC_address/%s/MAC_address_%d"%(d, attacker_num+n)
        if not os.path.isfile(analysis_file):
            read_pcap(n, attacker_num, rate, d)
        (specificity, precision, accuracy, test_2) = cuckoo2_method(n, attacker_num, rate, s, analysis_file, MAC_file)
        output_file_cuckoo_2.write("%d %f %f %f\n"% (attacker_num, specificity, precision, accuracy))
        if(test_2 is False):
            print('test _2 is false in %s/n%d_m%d_r%s.txt file' %(d, n, attacker_num, rate))
        (specificity, precision, accuracy, test_1, test_3) = bloom_method(n, attacker_num, rate, e, analysis_file, threshold, True)
        output_file_bloom.write("%d %f %f %f\n"% (attacker_num, specificity, precision, accuracy))
        if(test_1 is False):
            print('test _1 is false in %s/n%d_m%d_r%s.txt file' %(d, n, attacker_num, rate))

if __name__ == '__main__':
    call_method()