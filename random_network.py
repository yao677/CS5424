import networkx as nx
import matplotlib.pyplot as plt
import random as rd
import time


# add attributes to nodes in the network


# generate attributes for a random node

def create_attr():
    "the attributes are enclosed in a dictionary"
    attr_dict={}
    #38% to be in party A, 32% in party B, 30% in party N
    #Party A-> Democrats, Party B-> Republican, Party N-> Neutral 
    rd_num=rd.uniform(0,1)
    if rd_num<0.38:
        attr_dict["party"]="A"
    elif 0.38<=rd_num<0.7:
        attr_dict["party"]="B"
    else:
        attr_dict["party"]="N"
    
    #emotional state, key is "emot"
    #"C"-> calm, "A"-> agitated
    rd_num=rd.uniform(0,1)
    if attr_dict["party"]=="N":
        attr_dict["emot"]=="C"
    else:
        if rd_num<0.5:
            attr_dict["emot"]="C"
        else:
            attr_dict["emot"]="A"
    
    #probability of voting for party A
    attr_dict["p"]=0.5

    #state of a person with repsect to a piece of information
    #S-> uninformed, I-> informed & active , R-> informed & inactive
    rd_num=rd.randint(1,3)
    if rd_num==1:
        attr_dict["Info"]="S"
    elif rd_num==2:
        attr_dict["Info"]="I"
    else:
        attr_dict["Info"]="R"

    return attr_dict

# draw graph function
def draw_graph(graph, labels=None, graph_layout='shell',
               node_size=10, node_color='blue', node_alpha=0.3,
               node_text_size=12,
               edge_color='blue', edge_alpha=0.3, edge_tickness=1,
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
    plt.show()

def color_seq(graph):
    #draw nodes, blue for party A, red for party B, grey for party N
    color_list=[]
    for i in range(nx.number_of_nodes(graph)):
        if attr_dict["party"]=="A":
            color_list.append("red")
        elif attr_dict["party"]=="B":
            color_list.append("blue")
        else:
            color_list.append("grey")
    return color_list    

def main():
    #record start time
    start_time=time.time()

    # generate a random graph
    #Our sample network consists of 100,000 nodes, and average connectivity of node
    #ranges from 5 to 25

    num_nodes=100
    avg_degree=rd.randint(5,25)
    num_edges=num_nodes*avg_degree/2
    seed=7
    G=nx.dense_gnm_random_graph(num_nodes,num_edges,seed)

    #assign attributes to nodes in the network
    for i in range(100):
        attr_dict=create_attr()
        for key in attr_dict.keys():
            nx.set_node_attributes(G, key, attr_dict[key])

    draw_graph(G,graph_layout='random')
    print(G.nodes())
    print("--- %s seconds ---" % (time.time() - start_time))


main()
