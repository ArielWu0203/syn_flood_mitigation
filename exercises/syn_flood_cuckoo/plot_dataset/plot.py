import matplotlib.pyplot as plt
import numpy as np
import click

@click.command()
@click.option('-sc',help='scenario', type=click.INT)
def plot(sc):
    if(sc==2):
        plot_secerio_2()
    elif(sc==3):
        plot_secerio_3()
    elif(sc==5):
        plot_secerio_5()

def plot_secerio_2():
    fig_1 = plt.figure(figsize=(10,5))
    ax_1 = fig_1.add_subplot(1, 1, 1)
    ax_1.set_xlabel("# of attackers")
    ax_1.set_ylabel("specificity")
    fig_2 = plt.figure(figsize=(10,5))
    ax_2 = fig_2.add_subplot(1, 1, 1)
    ax_2.set_xlabel("# of attackers")
    ax_2.set_ylabel("prcision")
    fig_3 = plt.figure(figsize=(10,5))
    ax_3 = fig_3.add_subplot(1, 1, 1)
    ax_3.set_xlabel("# of attackers")
    ax_3.set_ylabel("accuracy")
    input_bloom=open("./bloom/n%d_ru%d_s2.txt"%(40, 10000), 'r')
    input_cuckoo=open("./cuckoo2/n%d_ru%d_s2.txt"%(40, 10000), 'r')
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
    fig_1.savefig("senerio_2_specificity.png")
    fig_2.savefig("senerio_2_precision.png")
    fig_3.savefig("senerio_2_accuracy.png")

def plot_secerio_3():
    fig_1 = plt.figure(figsize=(10,5))
    ax_1 = fig_1.add_subplot(1, 1, 1)
    ax_1.set_xlabel("# of attackers")
    ax_1.set_ylabel("specificity")
    fig_2 = plt.figure(figsize=(10,5))
    ax_2 = fig_2.add_subplot(1, 1, 1)
    ax_2.set_xlabel("# of attackers")
    ax_2.set_ylabel("prcision")
    fig_3 = plt.figure(figsize=(10,5))
    ax_3 = fig_3.add_subplot(1, 1, 1)
    ax_3.set_xlabel("# of attackers")
    ax_3.set_ylabel("accuracy")
    input_bloom=open("./bloom/n%d_ru%d_s3.txt"%(40, 200000), 'r')
    input_cuckoo=open("./cuckoo2/n%d_ru%d_s3.txt"%(40, 200000), 'r')
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
    fig_1.savefig("senerio_3_specificity.png")
    fig_2.savefig("senerio_3_precision.png")
    fig_3.savefig("senerio_3_accuracy.png")

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