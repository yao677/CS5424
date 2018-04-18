import networkx as nx
import matplotlib.pyplot as plt
import random as rd
import time

#record start time
start_time=time.time

# generate a random graph
#Our sample network consists of 100,000 nodes, and average connectivity of node
#ranges from 5 to 25

num_nodes=100000
avg_degree=rd.randint(5,25)
num_edges=num_nodes*avg_degree/2
seed=7
G=nx.dense_gnm_random_graph(num_nodes,num_edges,seed)


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
        graph_pos=nx.spring_layout(G)
    elif graph_layout == 'spectral':
        graph_pos=nx.spectral_layout(G)
    elif graph_layout == 'random':
        graph_pos=nx.random_layout(G)
    else:
        graph_pos=nx.shell_layout(G)



    #draw graph
    nx.draw_networkx_nodes(G,graph_pos,node_size=node_size,alpha=node_alpha, node_color=node_color)
    nx.draw_networkx_edges(G,graph_pos,width=edge_tickness,alpha=edge_alpha,edge_color=edge_color)
    nx.draw_networkx_labels(G, graph_pos,font_size=node_text_size,font_family=text_font)

    #show graph 
    plt.show()



#draw_graph(G,graph_layout='random')
print("--- %f seconds ---" % (time.time() - start_time))
