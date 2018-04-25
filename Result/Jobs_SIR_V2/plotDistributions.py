import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import os
import pickle

distributions = pickle.load(open("distributions.pkl", "rb"))

for i in range(len(distributions)) :
    plt.figure(i)
    plt.hist(distributions[i],50)
    plt.savefig("run" + str(i) + "_V2_distributionPlot.png")
