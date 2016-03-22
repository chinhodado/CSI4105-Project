import time

import matplotlib.pyplot as plt
import networkx as nx

# demo for the bruteforce algorithm
from algorithms.bruteforce_cycle import BruteforceCycle

bruteforce = BruteforceCycle()

graph = nx.complete_graph(9)
plt.figure("Original graph")
nx.draw_circular(graph, node_size=20)

start_time = time.time()
to_remove = bruteforce.get_fbvs(graph)
print(to_remove)
print("--- %s seconds ---" % (time.time() - start_time))
graph.remove_nodes_from(to_remove)

plt.figure("Processed graph")
nx.draw_circular(graph, node_size=20)
plt.show()
