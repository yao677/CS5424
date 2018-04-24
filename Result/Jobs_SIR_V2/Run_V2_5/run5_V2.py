import networkx as nx
#import matplotlib.pyplot as plt
import random as rd
import time
import generate_network as gn
import sys
import pickle

Pv = [
    [0.005, 0, 0, 0.005],
    [0.0025, -0.0025, -0.0025, 0],
    [0.0025, 0, -0.0025, 0],
    [0.0025, 0, -0.0025, 0.0025],
    [0, -0.005, -0.005, 0]
    ]

Pe = [
    [ ['AA', 1], ['AC', 1], ['AC', 0.12], ['AA', 1] ],
    [ ['AA', 1], ['AC', 1], ['AC', 1], ['AA', 0.87] ],
    [ ['NC', 1], ['NC', 1], ['NC', 1], ['NC', 1] ],
    [ ['BC', 1], ['BA', 0.87], ['BA', 1], ['BC', 1] ],
    [ ['BC', 0.12], ['BA', 1], ['BA', 1], ['BC', 1] ]
    ]

# generate attributes for a random node

def create_attr(probA, probB):
    "the attributes are enclosed in a dictionary"
    attr_dict={}
    #38% to be in party A, 32% in party B, 30% in party N
    #Party A-> Democrats, Party B-> Republican, Party N-> Neutral

    rd_num=rd.uniform(0,1)
    if rd_num<probA:
        if rd.uniform(0,1) < 0.5 :
            attr_dict["state"]="AA"
        else :
            attr_dict["state"]="AC"
        #attr_dict["p"]=0.87
    elif probA<=rd_num<(probA + probB):
        if rd.uniform(0,1) < 0.5 :
            attr_dict["state"]="BA"
        else :
            attr_dict["state"]="BC"
        #attr_dict["p"]=0.12
    else:
        attr_dict["state"]="NC"

    attr_dict["p"]=0.5

    #state of a person with repsect to a piece of information
    #S-> uninformed, I-> informed & active , R-> informed & inactive

    if rd.uniform(0,1)<0.7 : attr_dict["Info"]=["S"]
    else : attr_dict["Info"]=["I"]

    return attr_dict

def assign_attr(graph, probA, probB):
    "add attributes to nodes in a network"
    for i in range(nx.number_of_nodes(graph)):
        attr_dict=create_attr(probA, probB)
        graph.add_node(i, **attr_dict)


#SIR event in the network
def SIR(graph, infoTypes, pInfect, pRecover, pMediaEvent, pObserveMedia, infoDist):
    "A SIR event consits of I+S->I+I, I->R and S->I"

    global Pv
    global Pe

    infoCodes = {'GA':0, 'BA':1, 'GB':2, 'BB':3}
    partyCodes = {'AA':0, 'AC':1, 'NC':2, 'BC':3, 'BA':4}

    G=graph.copy()

    for i in range( len(infoTypes) ) :

        count = 0
        for node in G.nodes():

            neighbors=G.neighbors(node)

            #I->R
            if G.nodes[node]["Info"][i] == "I" :

                if rd.uniform(0,1) <= pRecover :
                    temp = G.nodes[node]["Info"].copy()
                    temp[i] = "R"
                    graph.add_node(node, Info=temp)

            #I+S->I+I, face to face information spreading
            if G.nodes[node]["Info"][i]=="S":

                for each in neighbors:

                    if G.node()[each]["Info"][i]=="I":

                        if rd.uniform(0,1) <= pInfect :

                            # MAKE THER PERSON INFECTED
                            temp = G.nodes[node]["Info"].copy()
                            temp[i] = "I"
                            graph.add_node(node, Info=temp)
                            count += 1

                            # UPDATE VOTING PROBABILITY
                            state = G.nodes[node]["state"]
                            rowIndex = partyCodes[state]
                            colIndex = infoCodes[infoTypes[i]]
                            temp = G.nodes[node]["p"]
                            temp += Pv[rowIndex][colIndex]
                            if temp > 1 : temp = 1
                            if temp < 0 : temp = 0
                            #G.nodes[node]["p"] += Pv[rowIndex][colIndex]
                            graph.add_node(node, p=temp)    # update voting prob

                            # UPDATE EMOTIONAL STATE
                            newState = Pe[rowIndex][colIndex][0]
                            probChange = Pe[rowIndex][colIndex][1]
                            if rd.uniform(0,1) <= probChange :
                                graph.add_node(node, state=newState)

                            break
            #print("Done node", count)
            count += 1

    #S->I (media interactions)
    if rd.uniform(0,1) <= pMediaEvent :  # does media event occur?

        infoTypes.append( getInfoType(infoDist) )

        for node in G :
            if rd.uniform(0,1) <= pObserveMedia :

                # media event is observed (make them infected)
                temp = graph.nodes[node]["Info"].copy()
                temp.append("I")
                graph.add_node(node, Info=temp)
                count += 1

                # UPDATE VOTING PROBABILITY
                state = G.nodes[node]["state"]
                rowIndex = partyCodes[state]
                colIndex = infoCodes[infoTypes[i]]
                temp = G.nodes[node]["p"]
                temp += Pv[rowIndex][colIndex]
                if temp > 1 : temp = 1
                if temp < 0 : temp = 0
                #G.nodes[node]["p"] += Pv[rowIndex][colIndex]
                graph.add_node(node, p=temp)    # update voting prob

                # UPDATE EMOTIONAL STATE
                newState = Pe[rowIndex][colIndex][0]
                probChange = Pe[rowIndex][colIndex][1]
                if rd.uniform(0,1) <= probChange :
                    graph.add_node(node, state=newState)

            else :
                # media event is not observed
                temp = graph.nodes[node]["Info"].copy()
                temp.append("S")
                graph.add_node(node, Info=temp)

    return count


# draw graph function
"""def draw_graph(graph, filename,labels=None, graph_layout='shell',
               node_size=40, node_color='blue', node_alpha=0.3,
               node_text_size=12,
               edge_color='black', edge_alpha=0.3, edge_tickness=0.5,
               edge_text_pos=0.3,
               text_font='sans-serif'):
    # these are different layouts for the network you may try
    # shell seems to work best

    if graph_layout == 'spring':
        graph_pos=nx.spring_layout(graph)
    elif graph_layout == 'spectral':
        graph_pos=nx.spectral_layout(graph)
    elif graph_layout == 'random':
        graph_pos=nx.random_layout(graph)
    else:
        graph_pos=nx.shell_layout(graph)

    #draw graph
    #assign node color
    node_color=color_seq(graph)
    nx.draw_networkx_nodes(graph,graph_pos,node_size=node_size,alpha=node_alpha, node_color=node_color)
    nx.draw_networkx_edges(graph,graph_pos,width=edge_tickness,alpha=edge_alpha,edge_color=edge_color)
    nx.draw_networkx_labels(graph, graph_pos,font_size=node_text_size,font_family=text_font)

    #show graph
    plt.savefig(filename)
    plt.close()


def color_seq(graph):
    #draw nodes, blue for party A, red for party B, grey for party N
    color_list=[]
    for i in range(nx.number_of_nodes(graph)):
        person=graph.nodes[i]
        if person["Info"][0]=="I":
            color_list.append("red")
        elif person["Info"][0]=="S":
            color_list.append("blue")
        else:
            color_list.append("green")
    return color_list"""

def election(graph) :
    """ simulate the election """
    votesA, votesB = 0, 0

    for node in graph :
        # draw rand num, if below voting prob for cand A, vote A, else vote B
        if graph.nodes[node]["p"] >= rd.uniform(0,1) : votesA += 1
        else : votesB += 1

    """print("Tallies: \n\tCandidate A:", votesA, "\n\tCandidate B:", votesB)
    if votesA > votesB : print("Candidate A Wins!")
    else : print("Candidate B Wins!")"""

    if votesA > votesB : print("A")
    else : print("B")

    return

def getInfoType(dist) :
    return rd.choices(['GA', 'BA', 'GB', 'BB'], dist)[0]

def main():
    #record start time
    start_time=time.time()

    inputFile = str(sys.argv[1])
    outputFile = str(sys.argv[0][:-3]) + "_" + str(sys.argv[2]) + str(sys.argv[3])+ ".pkl"

    # generate a random graph
    #Our sample network consists of 100,000 nodes, and average connectivity of node
    #ranges from 5 to 25

    # PARAMETERS
    days = 100
    probA = 0.50        # probability of being in party A
    probB = 0.20        # probability of being in party B
    pInfect = 0.4       # probability of receiving info from another individual
    pRecover = 0.2      # probability of stopping the spread of information
    pMediaEvent = 0.7   # probability a media event occurs
    pObserveMedia = 0.2 # probability of observing a media event

    #infoDist = [0.25, 0.25, 0.25, 0.25]         # Run 1
    #infoDist = [0.233, 0.233, 0.3, 0.233]       # Run 2
    #infoDist = [0.217, 0.217, 0.35, 0.217]      # Run 3
    #infoDist = [0.2, 0.2, 0.4, 0.2]             # Run 4
    infoDist = [0.183, 0.183, 0.45, 0.183]      # Run 5
    #infoDist = [0.233, 0.3, 0.233, 0.233]       # Run 6
    #infoDist = [0.217, 0.35, 0.217, 0.217]      # Run 7
    #infoDist = [0.2, 0.4, 0.2, 0.2]             # Run 8
    #infoDist = [0.183, 0.45, 0.183, 0.183]      # Run 9




    # stuff is array with seed value as first item and the network as second
    stuff = gn.read_network(inputFile)

    seedVal = stuff[0]
    #rd.seed(seedVal)

    G = stuff[1]

    #assign attributes to nodes in the network
    assign_attr(G, probA, probB)

    #rd.seed(rd.randint(0, 100000000000000))

    # initialization of information array
    infoTypes = [ getInfoType( infoDist ) ]

    #print("Done assigning", "--- %s seconds ---" % (time.time() - start_time))


    #print("info", infoTypes)
    #draw_graph(G,"beforeSIR")
    #count = 0
    for i in range(days) :
        SIR(G, infoTypes, pInfect, pRecover, pMediaEvent, pObserveMedia, infoDist)

    f = open(outputFile, "wb")
    pickle.dump(G, f)
        #print("DAY",i, "COMPLETE")
    #print("probabilites", [G.nodes[node]["p"] for node in G.nodes] )
    #print("info", infoTypes)
    #print(infoTypes.count("GA")/len(infoTypes),infoTypes.count("BA")/len(infoTypes),infoTypes.count("GB")/len(infoTypes),infoTypes.count("BB")/len(infoTypes))
    #print("COUNT =", count)
    #print(infoDist)
    #draw_graph(G,"afterSIR")
    election(G)

    #print("--- %s seconds ---" % (time.time() - start_time))


if __name__=="__main__":
    main()
