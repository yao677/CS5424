import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import os
import pickle

distributions = pickle.load(open("distributions.pkl", "rb"))

infoDist = [[0.25, 0.25, 0.25, 0.25],
            [0.233, 0.233, 0.3, 0.233],
            [0.217, 0.217, 0.35, 0.217],
            [0.2, 0.2, 0.4, 0.2],
            [0.183, 0.183, 0.45, 0.183],
            [0.233, 0.3, 0.233, 0.233],
            [0.217, 0.35, 0.217, 0.217],
            [0.2, 0.4, 0.2, 0.2],
            [0.183, 0.45, 0.183, 0.183]
            ]

for i in range(len(distributions)) :
    plt.figure(i)
    plt.xlim(0.1, 0.8)
    plt.ylim(0, 180000)
    plt.title("Distribution of Voting Probabilites \n Information Distribution = " + str(infoDist[i]))
    plt.xlabel("Probability of Voting for Candidate A")
    plt.ylabel("Number of Voters")
    plt.hist(distributions[i],50)
    plt.savefig("run" + str(i+1) + "_V2_distributionPlot.png")
