import networkx as nx
import time

from algorithms.bruteforce import Bruteforce
from algorithms.bruteforce_cycle import BruteforceCycle
from algorithms.iterative_compression import IterativeCompression
from algorithms.maximum_induced_forest import MaximumInducedForest
from algorithms.randomized import Randomized

"""
Test the algorithms using deterministic/pre-defined graphs with already known solution
"""


def test_algorithms(algorithms, graph, expected: int):
    for algorithm, name in algorithms:
        # make a copy of the graph in case the algorithm mutates it
        graph_copy = graph.copy()
        start_time = time.time()
        result = len(algorithm.get_fbvs(graph_copy))
        print("{0}: {1}, time: {2}".format(name, result, time.time() - start_time))
        assert expected == result, "Wrong result!"
    print()

bruteforce_cycle = BruteforceCycle()
bruteforce = Bruteforce()
ic = IterativeCompression()
rn = Randomized()
mif = MaximumInducedForest()

algorithms = [[bruteforce_cycle, "bruteforce_cycle"],
              [bruteforce, "bruteforce"],
              [ic, "itertive_compression"],
              # [rn, "randomized_opt"], # disabled because too slow
              [mif, "maximum_induced_forest"]]

print("Testing graph with 2 cycles that can be broken by removing 1 node (node 0)", end="\n")
graph = nx.Graph()
graph.add_cycle([0,1,2,3])
graph.add_cycle([0,3,4,5])
test_algorithms(algorithms, graph, 1)

print("Testing a custom graph with 1 cycle", end="\n")
graph = nx.Graph()
graph.add_nodes_from(range(1, 16))
graph.add_cycle([10,11,12])
test_algorithms(algorithms, graph, 1)

for i in range(3, 15):
    print("Testing a K{} complete graph".format(i), end="\n")
    graph = nx.complete_graph(i)
    test_algorithms(algorithms, graph, i - 2)

for i in range(5, 8):
    print("Testing an acyclic graph (star{})".format(i), end="\n")
    graph = nx.star_graph(i)
    test_algorithms(algorithms, graph, 0)
