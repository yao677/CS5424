import networkx as nx
import matplotlib.pyplot as plt
import random as rd
import time


Pv = [
    [0.00025, 0, 0, 0.00025],
    [0.0005, -0.0005, -0.0005, 0],
    [0.0005, 0, -0.0005, 0],
    [0. , 0, -0.0005, 0.0005],
    [0, -0.00025, -0.00025, 0]
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
    elif probA<=rd_num<(probA + probB):
        if rd.uniform(0,1) < 0.5 :
            attr_dict["state"]="BA"
        else :
            attr_dict["state"]="BC"
    else:
        attr_dict["state"]="NC"

    #probability of voting for party A
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
def SIR(graph, infoTypes):
    "A SIR event consits of I+S->I+I, I->R and S->I"

    global Pv
    global Pe

    infoCodes = {'GA':0, 'BA':1, 'GB':2, 'BB':3}
    partyCodes = {'AA':0, 'AC':1, 'NC':2, 'BC':3, 'BA':4}

    G=graph.copy()

    #I+S->I+I, face to face information spreading
    for i in range( len(infoTypes) ) :

        for node in G.nodes():
            neighbors=G.neighbors(node)
            if G.nodes[node]["Info"][i]=="S":
                for each in neighbors:
                    if G.node()[each]["Info"][i]=="I":
                        temp = G.nodes[node]["Info"]
                        temp[i] = "I"
                        graph.add_node(node, Info=temp) # update to infected

                        # UPDATE VOTING PROBABILITY
                        #state = G.nodes[node]["party"] + G.nodes[node]["emot"]
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

            #I->R


            #S->I


# draw graph function
def draw_graph(graph, filename,labels=None, graph_layout='shell',
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
        person=graph.node[i]
        if person["Info"]=="I":
            color_list.append("red")
        elif person["Info"]=="S":
            color_list.append("blue")
        else:
            color_list.append("green")
    return color_list

def main():
    #record start time
    start_time=time.time()

    # generate a random graph
    #Our sample network consists of 100,000 nodes, and average connectivity of node
    #ranges from 5 to 25

    seedVal=7
    rd.seed(seedVal)

    # PARAMETERS
    num_nodes=10    # for testing only
    #avg_degree=rd.randint(5,25)
    #num_edges=num_nodes*avg_degree/2
    num_edges = 10     # for testing only
    probA = 0.38
    probB = 0.32
    infoTypes = [ rd.choice(['GA', 'BA', 'GB', 'BB']) ]



    G=nx.dense_gnm_random_graph(num_nodes,num_edges,seedVal)

    #assign attributes to nodes in the network
    assign_attr(G, probA, probB)
    #draw graph
    print("info", infoTypes)
    print("state before", [G.nodes[node]["state"] for node in G.nodes] )
    print("infos before", [G.nodes[node]["Info"] for node in G.nodes] )
    print("probs before", [G.nodes[node]["p"] for node in G.nodes] )
    draw_graph(G,"beforeSIR")
    SIR(G, infoTypes)
    print("state after", [G.nodes[node]["state"] for node in G.nodes] )
    print("infos after", [G.nodes[node]["Info"] for node in G.nodes] )
    print("probs after", [G.nodes[node]["p"] for node in G.nodes] )
    #draw graph after applying one SIR event
    draw_graph(G,"afterSIR")
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__=="__main__":
    main()
