import random
import click
import numpy as np
from collections import  Counter

@click.command()
@click.option('-n', help='Number of MAC address', type=click.INT)
def make_input(n):
    mac = '00:00:00:'
    set_mac = set()
    i = 0
    while(len(set_mac) != n):
            number = [0]*3
            number[0] = random.randint(0,255)
            number[1] = random.randint(0,255)
            number[2] = random.randint(0,255)
            hex_num = ['']*3
            hex_num[0] = hex(number[0])[2:].zfill(2)
            hex_num[1] = hex(number[1])[2:].zfill(2)
            hex_num[2] = hex(number[2])[2:].zfill(2)
            result = mac+hex_num[0]+':'+hex_num[1]+':'+hex_num[2]
            set_mac.add(result)
    for ele in set_mac:
        print(ele)

if __name__ == '__main__':
    make_input()