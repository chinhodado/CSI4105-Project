import time

from algorithms.bruteforce import Bruteforce
from algorithms.dumb_bruteforce import DumbBruteforce
import networkx as nx

"""
Use some randomly-generated graphs to make sure the algorithms return the same value
"""


def test_algorithms(algorithms, graph):
    print()
    print("Testing graph with {0} nodes and {1} edges".format(graph.number_of_nodes(), graph.number_of_edges()))
    results = []
    for algorithm, name in algorithms:
        start_time = time.time()
        result = len(algorithm.get_fbvs(graph))
        print("{0}: {1}, time: {2}".format(name, result, time.time() - start_time))
        results.append(result)
    assert results.count(results[0]) == len(results), "The algorithms's results are not the same!"


bruteforce = Bruteforce()
dumb_bruteforce = DumbBruteforce()

algorithms = [[bruteforce, "bruteforce"], [dumb_bruteforce, "dumb_bruteforce"]]

graph = nx.erdos_renyi_graph(9, 0.5)
test_algorithms(algorithms, graph)

graph = nx.dense_gnm_random_graph(10, 25)
test_algorithms(algorithms, graph)

graph = nx.newman_watts_strogatz_graph(11, 5, 0.2)
test_algorithms(algorithms, graph)