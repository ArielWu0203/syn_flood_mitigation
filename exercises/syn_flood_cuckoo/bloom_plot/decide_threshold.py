import matplotlib.pyplot as plt
import numpy as np

def decide_threshold():
    fig_1 = plt.figure(figsize=(10,5))
    ax_1 = fig_1.add_subplot(1, 1, 1)
    ax_1.set_xlabel("Threshold")
    ax_1.set_ylabel("specificity")
    fig_2 = plt.figure(figsize=(10,5))
    ax_2 = fig_2.add_subplot(1, 1, 1)
    ax_2.set_xlabel("Threshold")
    ax_2.set_ylabel("precision")
    ax_1.xaxis.set_ticks(np.linspace(0.1, 2.0, num=20))       
    ax_2.xaxis.set_ticks(np.linspace(0.1, 2.0, num=20))       
    markers=["o", "^", "s", "*", "+", "D", "."]
    i=0
    for rate in [5, 10, 20, 40, 50, 80, 100]:
        f=open("n40_m40_ru%d.txt"%(1000000/rate), 'r')
        x=[]
        specificity_y=[]
        precision_y=[]
        for line in f.readlines():
            (T, specificity, precision) = [t(s) for t,s in zip((float,float,float),line.split())]
            x.append(T*10000)
            specificity_y.append(specificity)
            precision_y.append(precision)
        ax_1.plot(x, specificity_y, marker=markers[i])
        ax_2.plot(x, precision_y, marker=markers[i])
        i+=1
    legend=["5(f/s)","10(f/s)", "20(f/s)", "40(f/s)", "50(f/s)", "80(f/s)", "100(f/s)" ]
    ax_1.legend(legend)
    ax_2.legend(legend)
    fig_1.savefig("bloom_threshold_specificity_n40_m40.png")
    fig_2.savefig("bloom_threshold_precision_n40_m40.png")


if __name__ == '__main__':
    decide_threshold()