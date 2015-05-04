import numpy as np
import matplotlib.pyplot as plt
import sys
import warnings

colors = ['', 'Gold', 'Violet', 'LightSteelBlue', 'MediumBlue', 'Aqua', 'Crimson',\
    'Lime', 'Gray', 'SaddleBrown', 'HotPink', 'DarkGreen', 'CadetBlue']

fig = plt.figure()
plt.clf()
for i in range(4, 5):
    ax = fig.add_subplot(111)
    for j in range(12, 13):
        if i == j:
            continue
        d = "./results/s" + str(i) + "d" + str(j)+ "/"
        print d
        b = 660
        data = np.zeros(241)
        x_labels = np.zeros(241)
        iter_count = 0
        while b in range(660, 901):
            f = str(b)
            fname = d + f + "_loopless.txt"
            with warnings.catch_warnings():
               warnings.simplefilter("ignore")
               edges = np.loadtxt(fname, delimiter = "->", skiprows = 4)
            print "iter_count", iter_count
            data[iter_count] = len(edges)/2
            x_labels[iter_count] = float(b)/20
            iter_count += 1
            b += 1
        d = "./plots/"
        print data
        for z in range(0, len(data)):
            print x_labels[z], data[z]
        plt.plot(x_labels, data, label = str(j), linewidth = 2)
        axes = plt.gca()
        axes.set_xlim([32, 45])
    
#    handles, labels = ax.get_legend_handles_labels()
#    plt.legend(handles, labels, title = "Destination", loc = "lower right",\
#        prop = {'size': 10})
    plt.ylabel("Number of Valid Edges")
    plt.xlabel("Budget (ms)")
    plt.title("Flows from " + str(i) + " to " + str(j))
    plt.grid(b=True, which='minor', axis='xy')
    plt.savefig(d + "tc_flows_from_" + str(i) + ".png")
    plt.clf()
