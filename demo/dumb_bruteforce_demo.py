import time

import matplotlib.pyplot as plt
import networkx as nx

from algorithms.dumb_bruteforce import DumbBruteforce

# demo for the dumb bruteforce algorithm
dumb_bruteforce = DumbBruteforce()

graph = nx.complete_graph(9)
plt.figure("Original graph")
nx.draw_circular(graph, node_size=20)

start_time = time.time()
to_remove = dumb_bruteforce.get_fbvs(graph)
print(to_remove)
print("--- %s seconds ---" % (time.time() - start_time))
graph.remove_nodes_from(to_remove)

plt.figure("Processed graph")
nx.draw_circular(graph, node_size=20)
plt.show()
