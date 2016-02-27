import networkx as nx
import matplotlib.pyplot as plt

# can add nodes and edges manually
G = nx.Graph()
G.add_nodes_from([1,2,3])
G.add_edges_from([(1,2),(1,3),(2,3)])

# or generate graphs from built in methods
K_5 = nx.complete_graph(5)
er = nx.erdos_renyi_graph(20, 0.10)
red = nx.random_lobster(20, 0.5, 0.5)
star = nx.star_graph(10)

# draw and show
nx.draw_circular(star, node_size=20)
plt.show()