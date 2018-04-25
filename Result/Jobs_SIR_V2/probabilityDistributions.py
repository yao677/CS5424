import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import os
import pickle

dirs = []
for i in range(1,10) :
    dirs.append("Run_V2_" + str(i))

#for dir in dirs :
distributions = []
for dir in dirs :
    temp = []
    files = [file for file in os.listdir(dir) if file[-3:] == "pkl"]
    #print("look here", files)
    for filename in files :
        G = pickle.load(open(dir + "/" + filename, "rb"))
        temp2 = [G.nodes[node]["p"] for node in G.nodes]
        for item in temp2 :
            temp.append( item )
    distributions.append(temp)
    print("On to the next set")

pickle.dump(distributions, open("distributions.pkl", "wb"))
print( len(distributions) )
print( len(distributions[0]) )
