import matplotlib.pyplot as plt
import numpy as np
import click

@click.command()
@click.option('-sc',help='scenario', type=click.INT)
@click.option('-n', help='# of nomral users', type=click.INT)
@click.option('-m', help='# of attackers', type=click.INT)
@click.option('-r', help='rate of attack')
@click.option('-d', help='output data directory will store in which directory')
def plot(sc, n, m, r, d):
    if(sc==2):
        plot_secerio_2(n, r, d)
    elif(sc==3):
        plot_secerio_3(n, r, d)
    elif(sc==31):
        plot_secerio_3_1(n, r, d)
    elif(sc==4):
        plot_secerio_4(n, r, d)
    elif(sc==5):
        plot_secerio_5()

def plot_secerio_2(n, r, d):
    fig_1 = plt.figure(figsize=(10,5))
    ax_1 = fig_1.add_subplot(1, 1, 1)
    ax_1.set_xlabel("# of attackers")
    ax_1.set_ylabel("specificity")
    ax_1.set_ylim(0.0 ,1.1)
    fig_2 = plt.figure(figsize=(10,5))
    ax_2 = fig_2.add_subplot(1, 1, 1)
    ax_2.set_xlabel("# of attackers")
    ax_2.set_ylabel("prcision")
    ax_2.set_ylim(0.0 ,1.1)
    fig_3 = plt.figure(figsize=(10,5))
    ax_3 = fig_3.add_subplot(1, 1, 1)
    ax_3.set_xlabel("# of attackers")
    ax_3.set_ylabel("accuracy")
    ax_3.set_ylim(0.0 ,1.1)
    input_bloom=open("./bloom/%s/n%d_r%s_s2.txt"%(d, n, r), 'r')
    input_cuckoo=open("./cuckoo2/%s/n%d_r%s_s2.txt"%(d, n, r), 'r')
    x=[]
    specificity_y=[]
    precision_y=[]
    accuracy_y=[]
    for line in input_bloom.readlines():
        (num, specificity, precision, accuracy) = [t(s) for t,s in zip((int,float,float, float),line.split())]
        x.append(num)
        specificity_y.append(specificity)
        precision_y.append(precision)
        accuracy_y.append(accuracy)
    ax_1.plot(x, specificity_y, marker='o')
    ax_2.plot(x, precision_y, marker='o')
    ax_3.plot(x, accuracy_y, marker='o')
    x=[]
    specificity_y=[]
    precision_y=[]
    accuracy_y=[]
    for line in input_cuckoo.readlines():
        (num, specificity, precision, accuracy) = [t(s) for t,s in zip((int,float,float, float),line.split())]
        x.append(num)
        specificity_y.append(specificity)
        precision_y.append(precision)
        accuracy_y.append(accuracy)
    ax_1.plot(x, specificity_y, marker='^')
    ax_2.plot(x, precision_y, marker='^')
    ax_3.plot(x, accuracy_y, marker='^')
    legend=["bloom","our method"]
    ax_1.legend(legend)
    ax_2.legend(legend)
    ax_3.legend(legend)
    fig_1.savefig("./pic/%s/specificity.png" % d)
    fig_2.savefig("./pic/%s/precision.png" % d)
    fig_3.savefig("./pic/%s/accuracy.png" % d)

def plot_secerio_3(n, r, d):
    fig_1 = plt.figure(figsize=(10,5))
    ax_1 = fig_1.add_subplot(1, 1, 1)
    ax_1.set_xlabel("# of attackers")
    ax_1.set_ylabel("specificity")
    ax_1.set_ylim(0.0 ,1.1)
    fig_2 = plt.figure(figsize=(10,5))
    ax_2 = fig_2.add_subplot(1, 1, 1)
    ax_2.set_xlabel("# of attackers")
    ax_2.set_ylabel("prcision")
    ax_2.set_ylim(0.0 ,1.1)
    fig_3 = plt.figure(figsize=(10,5))
    ax_3 = fig_3.add_subplot(1, 1, 1)
    ax_3.set_xlabel("# of attackers")
    ax_3.set_ylabel("accuracy")
    ax_3.set_ylim(0.0 ,1.1)
    input_bloom=open("./bloom/%s/n%d_r%s_s3.txt"%(d, n, r), 'r')
    input_cuckoo=open("./cuckoo2/%s/n%d_r%s_s3.txt"%(d, n, r), 'r')
    x=[]
    specificity_y=[]
    precision_y=[]
    accuracy_y=[]
    for line in input_bloom.readlines():
        (num, specificity, precision, accuracy) = [t(s) for t,s in zip((int,float,float, float),line.split())]
        x.append(num)
        specificity_y.append(specificity)
        precision_y.append(precision)
        accuracy_y.append(accuracy)
    ax_1.plot(x, specificity_y, marker='o')
    ax_2.plot(x, precision_y, marker='o')
    ax_3.plot(x, accuracy_y, marker='o')
    x=[]
    specificity_y=[]
    precision_y=[]
    accuracy_y=[]
    for line in input_cuckoo.readlines():
        (num, specificity, precision, accuracy) = [t(s) for t,s in zip((int,float,float, float),line.split())]
        x.append(num)
        specificity_y.append(specificity)
        precision_y.append(precision)
        accuracy_y.append(accuracy)
    ax_1.plot(x, specificity_y, marker='^')
    ax_2.plot(x, precision_y, marker='^')
    ax_3.plot(x, accuracy_y, marker='^')
    legend=["bloom","our method"]
    ax_1.legend(legend)
    ax_2.legend(legend)
    ax_3.legend(legend)
    fig_1.savefig("./pic/%s/specificity.png" % d)
    fig_2.savefig("./pic/%s/precision.png" % d)
    fig_3.savefig("./pic/%s/accuracy.png" % d)

def plot_secerio_3_1(n, r, d):
    fig_1 = plt.figure(figsize=(10,5))
    ax_1 = fig_1.add_subplot(1, 1, 1)
    ax_1.set_xlabel("# of attackers")
    ax_1.set_ylabel("specificity")
    ax_1.set_ylim(0.0 ,1.1)
    fig_2 = plt.figure(figsize=(10,5))
    ax_2 = fig_2.add_subplot(1, 1, 1)
    ax_2.set_xlabel("# of attackers")
    ax_2.set_ylabel("prcision")
    ax_2.set_ylim(0.0 ,1.1)
    fig_3 = plt.figure(figsize=(10,5))
    ax_3 = fig_3.add_subplot(1, 1, 1)
    ax_3.set_xlabel("# of attackers")
    ax_3.set_ylabel("accuracy")
    ax_3.set_ylim(0.0 ,1.1)
    input_bloom=open("./bloom/%s/n%d_r%s_s3_1.txt"%(d, n, r), 'r')
    input_bloom_none_T=open("./bloom/%s/n%d_r%s_s3_1_none_T.txt"%(d, n, r), 'r')
    input_cuckoo=open("./cuckoo2/%s/n%d_r%s_s3.txt"%(d, n, r), 'r')
    x=[]
    specificity_y=[]
    precision_y=[]
    accuracy_y=[]
    for line in input_bloom.readlines():
        (num, specificity, precision, accuracy) = [t(s) for t,s in zip((int,float,float, float),line.split())]
        x.append(num)
        specificity_y.append(specificity)
        precision_y.append(precision)
        accuracy_y.append(accuracy)
    ax_1.plot(x, specificity_y, marker='o')
    ax_2.plot(x, precision_y, marker='o')
    ax_3.plot(x, accuracy_y, marker='o')
    x=[]
    specificity_y=[]
    precision_y=[]
    accuracy_y=[]
    for line in input_bloom_none_T.readlines():
        (num, specificity, precision, accuracy) = [t(s) for t,s in zip((int,float,float, float),line.split())]
        x.append(num)
        specificity_y.append(specificity)
        precision_y.append(precision)
        accuracy_y.append(accuracy)
    ax_1.plot(x, specificity_y, marker='+')
    ax_2.plot(x, precision_y, marker='+')
    ax_3.plot(x, accuracy_y, marker='+')
    x=[]
    specificity_y=[]
    precision_y=[]
    accuracy_y=[]
    for line in input_cuckoo.readlines():
        (num, specificity, precision, accuracy) = [t(s) for t,s in zip((int,float,float, float),line.split())]
        x.append(num)
        specificity_y.append(specificity)
        precision_y.append(precision)
        accuracy_y.append(accuracy)
    ax_1.plot(x, specificity_y, marker='^')
    ax_2.plot(x, precision_y, marker='^')
    ax_3.plot(x, accuracy_y, marker='^')
    legend=["bloom","bloom without decreasing", "our method"]
    ax_1.legend(legend)
    ax_2.legend(legend)
    ax_3.legend(legend)
    fig_1.savefig("./pic/%s/specificity_without_decreasing.png" % d)
    fig_2.savefig("./pic/%s/precision_without_decreasing.png" % d)
    fig_3.savefig("./pic/%s/accuracy_without_decreasing.png" % d)

def plot_secerio_4(n, r, d):
    fig_1 = plt.figure(figsize=(10,5))
    ax_1 = fig_1.add_subplot(1, 1, 1)
    ax_1.set_xlabel("# of attackers")
    ax_1.set_ylabel("specificity")
    ax_1.set_ylim(0.0 ,1.1)
    fig_2 = plt.figure(figsize=(10,5))
    ax_2 = fig_2.add_subplot(1, 1, 1)
    ax_2.set_xlabel("# of attackers")
    ax_2.set_ylabel("prcision")
    ax_2.set_ylim(0.0 ,1.1)
    fig_3 = plt.figure(figsize=(10,5))
    ax_3 = fig_3.add_subplot(1, 1, 1)
    ax_3.set_xlabel("# of attackers")
    ax_3.set_ylabel("accuracy")
    ax_3.set_ylim(0.0 ,1.1)
    input_bloom=open("./bloom/%s/n%d_r%s_s4.txt"%(d, n, r), 'r')
    input_cuckoo=open("./cuckoo2/%s/n%d_r%s_s4.txt"%(d, n, r), 'r')
    x=[]
    specificity_y=[]
    precision_y=[]
    accuracy_y=[]
    for line in input_bloom.readlines():
        (num, specificity, precision, accuracy) = [t(s) for t,s in zip((int,float,float, float),line.split())]
        x.append(num)
        specificity_y.append(specificity)
        precision_y.append(precision)
        accuracy_y.append(accuracy)
    ax_1.plot(x, specificity_y, marker='o')
    ax_2.plot(x, precision_y, marker='o')
    ax_3.plot(x, accuracy_y, marker='o')
    x=[]
    specificity_y=[]
    precision_y=[]
    accuracy_y=[]
    for line in input_cuckoo.readlines():
        (num, specificity, precision, accuracy) = [t(s) for t,s in zip((int,float,float, float),line.split())]
        x.append(num)
        specificity_y.append(specificity)
        precision_y.append(precision)
        accuracy_y.append(accuracy)
    ax_1.plot(x, specificity_y, marker='^')
    ax_2.plot(x, precision_y, marker='^')
    ax_3.plot(x, accuracy_y, marker='^')
    legend=["bloom","our method"]
    ax_1.legend(legend)
    ax_2.legend(legend)
    ax_3.legend(legend)
    fig_1.savefig("./pic/%s/specificity.png" % d)
    fig_2.savefig("./pic/%s/precision.png" % d)
    fig_3.savefig("./pic/%s/accuracy.png" % d)

def plot_secerio_5():
    fig_1 = plt.figure(figsize=(10,5))
    ax_1 = fig_1.add_subplot(1, 1, 1)
    ax_1.set_xlabel("# of normal users")
    ax_1.set_ylabel("specificity")
    fig_2 = plt.figure(figsize=(10,5))
    ax_2 = fig_2.add_subplot(1, 1, 1)
    ax_2.set_xlabel("# of normal users")
    ax_2.set_ylabel("prcision")
    fig_3 = plt.figure(figsize=(10,5))
    ax_3 = fig_3.add_subplot(1, 1, 1)
    ax_3.set_xlabel("# of normal users")
    ax_3.set_ylabel("accuracy")
    input_bloom=open("./bloom/m%d_ru%d_s5.txt"%(40, 200000), 'r')
    input_cuckoo=open("./cuckoo2/m%d_ru%d_s5.txt"%(40, 200000), 'r')
    x=[]
    specificity_y=[]
    precision_y=[]
    accuracy_y=[]
    for line in input_bloom.readlines():
        (num, specificity, precision, accuracy) = [t(s) for t,s in zip((int,float,float, float),line.split())]
        x.append(num)
        specificity_y.append(specificity)
        precision_y.append(precision)
        accuracy_y.append(accuracy)
    ax_1.plot(x, specificity_y, marker='o')
    ax_2.plot(x, precision_y, marker='o')
    ax_3.plot(x, accuracy_y, marker='o')
    x=[]
    specificity_y=[]
    precision_y=[]
    accuracy_y=[]
    for line in input_cuckoo.readlines():
        (num, specificity, precision, accuracy) = [t(s) for t,s in zip((int,float,float, float),line.split())]
        x.append(num)
        specificity_y.append(specificity)
        precision_y.append(precision)
        accuracy_y.append(accuracy)
    ax_1.plot(x, specificity_y, marker='^')
    ax_2.plot(x, precision_y, marker='^')
    ax_3.plot(x, accuracy_y, marker='^')
    legend=["bloom","method"]
    ax_1.legend(legend)
    ax_2.legend(legend)
    ax_3.legend(legend)
    fig_1.savefig("senerio_5_specificity.png")
    fig_2.savefig("senerio_5_precision.png")
    fig_3.savefig("senerio_5_accuracy.png")

if __name__ == '__main__':
    plot()