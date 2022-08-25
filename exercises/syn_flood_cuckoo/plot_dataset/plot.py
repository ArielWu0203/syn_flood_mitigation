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
        plot_secerio_for_attacker(n, r, d, 'sc2')
        plot_all_for_attacker(n, r, 'sc2')
    elif(sc==5):
        plot_secerio_for_attacker(n, r, d, 'sc5')
        # plot_secerio_5_1(n, r, d)
        plot_all_for_attacker(n, r, 'sc5')
    elif(sc==6):
        plot_secerio_for_normal(m, r, d, 'sc6')
        plot_all_for_normal(m, r, 'sc6')
    elif(sc==7):
        plot_secerio_for_normal(m, r, d, 'sc7')
        plot_all_for_normal(m, r, 'sc7')

def plot_all_for_normal(m, r, sc):
    fig_1 = plt.figure(figsize=(10,5))
    ax_1 = fig_1.add_subplot(1, 1, 1)
    ax_1.set_xlabel("# of normal users")
    ax_1.set_ylabel("specificity")
    ax_1.set_ylim(0.0 ,1.1)
    fig_2 = plt.figure(figsize=(10,5))
    ax_2 = fig_2.add_subplot(1, 1, 1)
    ax_2.set_xlabel("# of normal users")
    ax_2.set_ylabel("prcision")
    ax_2.set_ylim(0.0 ,1.1)
    fig_3 = plt.figure(figsize=(10,5))
    ax_3 = fig_3.add_subplot(1, 1, 1)
    ax_3.set_xlabel("# of normal users")
    ax_3.set_ylabel("accuracy")
    ax_3.set_ylim(0.0 ,1.1)
    all_file_names=[]
    markers=[]
    legend=[]
    if(sc=="sc6"):
        all_file_names= ["./bloom/%s/data_%d/m%d_r%s_s6.txt", "./cuckoo2/%s/data_%d/m%d_r%s_s6.txt"]
        markers=[".", "o"]
        markerfacecolors=['b', 'none']
        markersizes=[8,9]
        legend=["bloom", "our method"]
    if(sc=="sc7"):
        all_file_names= ["./bloom/%s/data_%d/m%d_r%s_s7_1_none_T.txt", "./cuckoo2/%s/data_%d/m%d_r%s_s7.txt"]
        markers=[".", "o"]
        markersizes=[8,9]
        markerfacecolors=['b', 'none']
        legend=["bloom", "our method"]
    for file_name, marker, markerfacecolor, markersize in zip(all_file_names, markers, markerfacecolors, markersizes):
        x=[20, 30, 40, 50 ,60 , 70]
        specificity_y=[0.0]*6
        precision_y=[0.0]*6
        accuracy_y=[0.0]*6
        for i in range(1, 11):
            file=open(file_name %(sc, i, m, r), 'r')
            line_num=0
            for line in file.readlines():
                (num, specificity, precision, accuracy) = [t(s) for t,s in zip((int,float,float, float),line.split())]
                specificity_y[line_num]+=specificity
                precision_y[line_num]+=precision
                accuracy_y[line_num]+=accuracy
                line_num+=1
        ax_1.plot(x, [y/10 for y in specificity_y], marker=marker,  markerfacecolor=markerfacecolor, markersize=markersize)
        ax_2.plot(x, [y/10 for y in precision_y], marker=marker,  markerfacecolor=markerfacecolor, markersize=markersize)
        ax_3.plot(x, [y/10 for y in accuracy_y], marker=marker,  markerfacecolor=markerfacecolor, markersize=markersize)
    ax_1.legend(legend)
    ax_1.set_ylim(0.8,1.05)
    ax_1.set_yticks(np.arange(0.8, 1.05, 0.05))
    ax_2.legend(legend)
    ax_2.set_ylim(0.8,1.05)
    ax_2.set_yticks(np.arange(0.8, 1.05, 0.05))
    ax_3.legend(legend)
    ax_3.set_ylim(0.8,1.05)
    ax_3.set_yticks(np.arange(0.8, 1.05, 0.05))
    fig_1.savefig("./pic/%s/specificity.png" % sc)
    fig_2.savefig("./pic/%s/precision.png" % sc)
    fig_3.savefig("./pic/%s/accuracy" % sc)

def plot_secerio_for_normal(m, r, d, sc):
    fig_1 = plt.figure(figsize=(10,5))
    ax_1 = fig_1.add_subplot(1, 1, 1)
    ax_1.set_xlabel("# of normal users")
    ax_1.set_ylabel("specificity")
    ax_1.set_ylim(0.0 ,1.1)
    fig_2 = plt.figure(figsize=(10,5))
    ax_2 = fig_2.add_subplot(1, 1, 1)
    ax_2.set_xlabel("# of normal users")
    ax_2.set_ylabel("prcision")
    ax_2.set_ylim(0.0 ,1.1)
    fig_3 = plt.figure(figsize=(10,5))
    ax_3 = fig_3.add_subplot(1, 1, 1)
    ax_3.set_xlabel("# of normal users")
    ax_3.set_ylabel("accuracy")
    ax_3.set_ylim(0.0 ,1.1)
    input_bloom_name=""
    input_cuckoo_name=""
    if(sc=="sc6"):
        input_bloom_name="./bloom/%s/m%d_r%s_s6.txt"
        input_cuckoo_name="./cuckoo2/%s/m%d_r%s_s6.txt"
    elif(sc=="sc7"):
        input_bloom_name="./bloom/%s/m%d_r%s_s7.txt"
        input_cuckoo_name="./cuckoo2/%s/m%d_r%s_s7.txt"
    input_bloom=open(input_bloom_name %(d, m, r), 'r')
    input_cuckoo=open(input_cuckoo_name %(d, m, r), 'r')
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
    ax_1.plot(x, specificity_y, marker='.',  markerfacecolor='b', markersize=8)
    ax_2.plot(x, precision_y, marker='.',  markerfacecolor='b', markersize=8)
    ax_3.plot(x, accuracy_y, marker='.',  markerfacecolor='b', markersize=8)
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
    ax_1.plot(x, specificity_y, marker='o',  markerfacecolor='none', markersize=9)
    ax_2.plot(x, precision_y, marker='o',  markerfacecolor='none', markersize=9)
    ax_3.plot(x, accuracy_y, marker='o',  markerfacecolor='none', markersize=9)
    legend=["bloom","our method"]
    ax_1.legend(legend)
    ax_1.set_ylim(0.8,1.05)
    ax_1.set_yticks(np.arange(0.8, 1.05, 0.05))
    ax_2.legend(legend)
    ax_2.set_ylim(0.8,1.05)
    ax_2.set_yticks(np.arange(0.8, 1.05, 0.05))
    ax_3.legend(legend)
    ax_3.set_ylim(0.8,1.05)
    ax_3.set_yticks(np.arange(0.8, 1.05, 0.05))
    fig_1.savefig("./pic/%s/specificity.png" % d)
    fig_2.savefig("./pic/%s/precision.png" % d)
    fig_3.savefig("./pic/%s/accuracy.png" % d)

def plot_secerio_for_attacker(n, r, d, sc):
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
    input_bloom_name=""
    input_cuckoo_name=""
    if(sc=="sc2"):
        input_bloom_name="./bloom/%s/n%d_r%s_s2.txt"
        input_cuckoo_name="./cuckoo2/%s/n%d_r%s_s2.txt"
    elif(sc=="sc5"):
        input_bloom_name="./bloom/%s/n%d_r%s_s5.txt"
        input_cuckoo_name="./cuckoo2/%s/n%d_r%s_s5.txt"
    input_bloom=open(input_bloom_name %(d, n, r), 'r')
    input_cuckoo=open(input_cuckoo_name %(d, n, r), 'r')
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
    ax_1.plot(x, specificity_y, marker='.',  markerfacecolor='b', markersize=8)
    ax_2.plot(x, precision_y, marker='.',  markerfacecolor='b', markersize=8)
    ax_3.plot(x, accuracy_y, marker='.',  markerfacecolor='b', markersize=8)
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
    ax_1.plot(x, specificity_y, marker='o',  markerfacecolor='none', markersize=9)
    ax_2.plot(x, precision_y, marker='o',  markerfacecolor='none', markersize=9)
    ax_3.plot(x, accuracy_y, marker='o',  markerfacecolor='none', markersize=9)
    legend=["bloom","our method"]
    ax_1.legend(legend)
    ax_1.set_ylim(0.8,1.05)
    ax_1.set_yticks(np.arange(0.8, 1.05, 0.05))
    ax_2.legend(legend)
    ax_2.set_ylim(0.8,1.05)
    ax_2.set_yticks(np.arange(0.8, 1.05, 0.05))
    ax_3.legend(legend)
    ax_3.set_ylim(0.8,1.05)
    ax_3.set_yticks(np.arange(0.8, 1.05, 0.05))
    fig_1.savefig("./pic/%s/specificity.png" % d)
    fig_2.savefig("./pic/%s/precision.png" % d)
    fig_3.savefig("./pic/%s/accuracy.png" % d)

def plot_secerio_5_1(n, r, d):
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
    input_bloom=open("./bloom/%s/n%d_r%s_s5_1.txt"%(d, n, r), 'r')
    input_bloom_none_T=open("./bloom/%s/n%d_r%s_s5_1_none_T.txt"%(d, n, r), 'r')
    input_cuckoo=open("./cuckoo2/%s/n%d_r%s_s5.txt"%(d, n, r), 'r')
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
    ax_1.plot(x, specificity_y, marker='.',  markerfacecolor='none')
    ax_2.plot(x, precision_y, marker='.',  markerfacecolor='none')
    ax_3.plot(x, accuracy_y, marker='.',  markerfacecolor='none')
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
    ax_1.plot(x, specificity_y, marker='^', markerfacecolor='none')
    ax_2.plot(x, precision_y, marker='^', markerfacecolor='none')
    ax_3.plot(x, accuracy_y, marker='^', markerfacecolor='none')
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
    ax_1.plot(x, specificity_y, marker='^',  markerfacecolor='none')
    ax_2.plot(x, precision_y, marker='^',  markerfacecolor='none')
    ax_3.plot(x, accuracy_y, marker='^',  markerfacecolor='none')
    legend=["bloom","bloom without decreasing", "our method"]
    ax_1.legend(legend)
    ax_1.set_ylim(0.8,1.05)
    ax_1.set_yticks(np.arange(0.8, 1.05, 0.05))
    ax_2.legend(legend)
    ax_2.set_ylim(0.8,1.05)
    ax_2.set_yticks(np.arange(0.8, 1.05, 0.05))
    ax_3.legend(legend)
    ax_3.set_ylim(0.8,1.05)
    ax_3.set_yticks(np.arange(0.8, 1.05, 0.05))
    fig_1.savefig("./pic/%s/specificity_without_decreasing.png" % d)
    fig_2.savefig("./pic/%s/precision_without_decreasing.png" % d)
    fig_3.savefig("./pic/%s/accuracy_without_decreasing.png" % d)

def plot_all_for_attacker(n, r, sc):
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
    all_file_names=[]
    markers=[]
    legend=[]
    if(sc=="sc2"):
        all_file_names= ["./bloom/%s/data_%d/n%d_r%s_s2.txt", "./cuckoo2/%s/data_%d/n%d_r%s_s2.txt"]
        markers=[".", "o"]
        markerfacecolors=['b', 'none']
        markersizes=[8, 9]
        legend=["bloom", "our method"]
    elif(sc=="sc5"):
        all_file_names= ["./bloom/%s/data_%d/n%d_r%s_s5_1_none_T.txt", "./cuckoo2/%s/data_%d/n%d_r%s_s5.txt"]
        markers=[".", "o"]
        markerfacecolors=['b', 'none']
        markersizes=[8, 9]
        legend=["bloom", "our method"]
    for file_name, marker, markerfacecolor, markersize in zip(all_file_names, markers, markerfacecolors, markersizes):
        x=[20, 30, 40, 50 ,60 , 70]
        specificity_y=[0.0]*6
        precision_y=[0.0]*6
        accuracy_y=[0.0]*6
        for i in range(1, 11):
            file=open(file_name %(sc, i, n, r), 'r')
            line_num=0
            for line in file.readlines():
                (num, specificity, precision, accuracy) = [t(s) for t,s in zip((int,float,float, float),line.split())]
                specificity_y[line_num]+=specificity
                precision_y[line_num]+=precision
                accuracy_y[line_num]+=accuracy
                line_num+=1
        specificity_y = [y/10 for y in specificity_y]
        precision_y =  [y/10 for y in precision_y]
        accuracy_y = [y/10 for y in accuracy_y]
        ax_1.plot(x, specificity_y, marker=marker, markerfacecolor=markerfacecolor, markersize=markersize)
        ax_2.plot(x, precision_y, marker=marker, markerfacecolor=markerfacecolor, markersize=markersize)
        ax_3.plot(x, accuracy_y, marker=marker, markerfacecolor=markerfacecolor, markersize=markersize)
    ax_1.legend(legend)
    ax_1.set_ylim(0.8,1.05)
    ax_1.set_yticks(np.arange(0.8, 1.05, 0.05))
    ax_2.legend(legend)
    ax_2.set_ylim(0.8,1.05)
    ax_2.set_yticks(np.arange(0.8, 1.05, 0.05))
    ax_3.legend(legend)
    ax_3.set_ylim(0.8,1.05)
    ax_3.set_yticks(np.arange(0.8, 1.05, 0.05))
    fig_1.savefig("./pic/%s/specificity.png" % sc)
    fig_2.savefig("./pic/%s/precision.png" % sc)
    fig_3.savefig("./pic/%s/accuracy" % sc)

if __name__ == '__main__':
    plot()