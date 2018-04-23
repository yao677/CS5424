import networkx as nx
import random as rd
import time
import pickle
import sys

def generate_network(seedVal,num_nodes,avg_degree):
    "Given network parameters, create the network and write it to a pickle file"
    #record start time
    start_time=time.time()

    #generate a random network
    rd.seed(seedVal)
    num_edges=num_nodes*avg_degree/2
    G=nx.dense_gnm_random_graph(num_nodes,num_edges,seedVal)

    #write to pickle series data
    filename = "network_node-%d_degree-%d_seed-%d.pkl" % (num_nodes,avg_degree,seedVal)
    pickle.dump([seedVal,G],open(filename,"wb"))
    print("--- %s seconds ---" % (time.time() - start_time))

def read_network(filename):
    "load network from a .pkl file"
    return pickle.load(open(filename,"rb"))

def main():
    print("Enter the arguements for generating a network")
    seedVal=input("Enter values for seedVal: ")
    num_nodes=input("Enter values for num_nodes: ")
    avg_degree=input("Enter values for avg_degree: ")

    generate_network(int(seedVal),int(num_nodes),int(avg_degree))


if __name__ == "__main__":
    main()
