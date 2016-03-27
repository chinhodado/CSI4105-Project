import time

import networkx as nx

from algorithms.bruteforce import Bruteforce
from algorithms.bruteforce_cycle import BruteforceCycle
from algorithms.iterative_compression import IterativeCompression

"""
Use some randomly-generated graphs to make sure the algorithms return the same value
"""


def test_algorithms(algorithms, graph: nx.Graph):
    print()
    print("Testing graph with {0} nodes and {1} edges".format(graph.number_of_nodes(), graph.number_of_edges()))
    results = []
    for algorithm, name in algorithms:
        start_time = time.time()
        result = len(algorithm.get_fbvs(graph))
        print("{0}: {1}, time: {2}".format(name, result, time.time() - start_time))
        results.append(result)
    assert results.count(results[0]) == len(results), "The algorithms's results are not the same!"


bruteforce_cycle = BruteforceCycle()
bruteforce = Bruteforce()
ic = IterativeCompression()

algorithms = [[bruteforce_cycle, "bruteforce_cycle"], [bruteforce, "bruteforce"], [ic, "itertive_compression"]]

graph = nx.erdos_renyi_graph(9, 0.5)
test_algorithms(algorithms, graph)

graph = nx.erdos_renyi_graph(10, 0.7)
test_algorithms(algorithms, graph)

graph = nx.erdos_renyi_graph(11, 0.6)
test_algorithms(algorithms, graph)

graph = nx.erdos_renyi_graph(12, 0.3)
test_algorithms(algorithms, graph)

graph = nx.erdos_renyi_graph(13, 0.5)
test_algorithms(algorithms, graph)

graph = nx.erdos_renyi_graph(15, 0.8)
test_algorithms(algorithms, graph)

graph = nx.erdos_renyi_graph(16, 0.8)
test_algorithms(algorithms, graph)

graph = nx.dense_gnm_random_graph(10, 25)
test_algorithms(algorithms, graph)

graph = nx.newman_watts_strogatz_graph(11, 5, 0.2)
test_algorithms(algorithms, graph)
