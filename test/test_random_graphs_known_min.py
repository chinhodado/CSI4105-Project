import inspect
import time
from networkx import Graph

from algorithms.iterative_compression import IterativeCompression
from tools.generate import generate_random_graph

"""
Use some randomly-generated graphs with already-known min size fbvs to test the algorithms
"""


def test_algorithms(algorithms, graph: Graph, k):
    print()
    print("Testing graph with {0} nodes and {1} edges".format(graph.number_of_nodes(), graph.number_of_edges()))

    for algorithm, name in algorithms:
        start_time = time.time()

        args = inspect.getfullargspec(algorithm)[0]
        if len(args) == 2:
            result = len(algorithm(graph))
        else:
            result = len(algorithm(graph, k))

        print("{0}: {1}, time: {2}".format(name, result, time.time() - start_time))
        assert k == result, "Wrong result!"


ic = IterativeCompression()

algorithms = [[ic.get_fbvs, "itertive_compression_opt"], [ic.get_fbvs_max_size, "itertive_compression_dec"]]

for k in range(1, 10):
    g = generate_random_graph(k)
    test_algorithms(algorithms, g, k)
