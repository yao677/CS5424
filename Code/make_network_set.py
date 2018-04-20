#create the set of networks for testing SIR
import generate_network as gnet

#parameter space definition
num_nodes_list=[50000,100000]
avg_degree_list=[5,10]
seedVal_list=[1,2,3,4,5]



def main() :
    global num_nodes_list, global avg_degree_list, global seedVal_list
    for i in num_nodes_list:
        for j in avg_degree_list:
            for k in seedVal_list:
                gnet.generate_network(i,j,k)

main()
