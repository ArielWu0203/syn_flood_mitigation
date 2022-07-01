import matplotlib.pyplot as plt
import numpy as np

def decide_threshold():
    fig_1 = plt.figure(figsize=(10,5))
    ax_1 = fig_1.add_subplot(1, 1, 1)
    ax_1.set_xlabel("threshold")
    ax_1.set_ylabel("specificity")
    fig_2 = plt.figure(figsize=(10,5))
    ax_2 = fig_2.add_subplot(1, 1, 1)
    ax_2.set_xlabel("threshold")
    ax_2.set_ylabel("precision")
    fig_3 = plt.figure(figsize=(10,5))
    ax_3 = fig_3.add_subplot(1, 1, 1)
    ax_3.set_xlabel("threshold")
    ax_3.set_ylabel("accuracy")
    ax_1.xaxis.set_ticks(np.linspace(0.1, 2.0, num=20))       
    ax_2.xaxis.set_ticks(np.linspace(0.1, 2.0, num=20))
    ax_3.xaxis.set_ticks(np.linspace(0.1, 2.0, num=20))
    markers=["o", "^", "s", "*", "+", "d"]
    i=0
    for rate in [ '4', '1', 'u200000', 'u100000', 'u66667', 'u50000']:
        f=open("n20_m20_r%s.txt"%(rate), 'r')
        x=[]
        specificity_y=[]
        precision_y=[]
        accuracy_y=[]
        for line in f.readlines():
            (T, specificity, precision, accuracy) = [t(s) for t,s in zip((float,float,float, float),line.split())]
            x.append(T)
            specificity_y.append(specificity)
            precision_y.append(precision)
            accuracy_y.append(accuracy)
        ax_1.plot(x, specificity_y, marker=markers[i])
        ax_2.plot(x, precision_y, marker=markers[i])
        ax_3.plot(x, accuracy_y, marker=markers[i])
        i+=1
    legend=["0.25(f/s)", "1(f/s)","5(f/s)", "10(f/s)", "15(f/s)", "20(f/s)"]
    box = ax_1.get_position()
    ax_1.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    ax_1.legend(legend, loc='center left', bbox_to_anchor=(1, 0.5))
    ax_2.legend(legend, loc='center left', bbox_to_anchor=(1, 0.5))
    ax_3.legend(legend, loc='center left', bbox_to_anchor=(1, 0.5))
    fig_1.savefig("bloom_threshold_specificity_n20_m20.png")
    fig_2.savefig("bloom_threshold_precision_n20_m20.png")
    fig_3.savefig("bloom_threshold_accuracy_n20_m20.png")


if __name__ == '__main__':
    decide_threshold()