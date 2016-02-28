import networkx as nx
import matplotlib.pyplot as plt
import sys
import time


def bruteforce(graph):
    """ Bruteforce to find the min size feedback vertex set
    This will return a set of vertex whose removal will make the graph acyclic
    """

    # get the list of cycles
    cycles = nx.cycle_basis(graph)

    if len(cycles) == 0:
        return set()

    # get the set of nodes that is in at least one cycle
    nodes_in_cycles = set([item for sublist in cycles for item in sublist])

    min_num_to_remove = sys.maxsize
    min_nodes_to_remove = set()

    for node in nodes_in_cycles:
        # make an induced subgraph with the current node removed
        nodes = graph.nodes()
        nodes.remove(node)
        new_graph = graph.subgraph(nodes)

        nodes_to_remove = bruteforce(new_graph)

        if len(nodes_to_remove) < min_num_to_remove:
            min_num_to_remove = len(nodes_to_remove)
            nodes_to_remove.add(node)
            min_nodes_to_remove = nodes_to_remove

    return min_nodes_to_remove

#graph = nx.complete_graph(7)
graph = nx.erdos_renyi_graph(8, 0.5)
start_time = time.time()
to_remove = bruteforce(graph)
print(to_remove)
print("--- %s seconds ---" % (time.time() - start_time))
graph.remove_nodes_from(to_remove)
nx.draw_circular(graph, node_size=20)
plt.show()
