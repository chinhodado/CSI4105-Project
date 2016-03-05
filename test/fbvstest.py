import networkx as nx

from algorithms.feedback_vertex_set_algorithm import FeedbackVertexSetAlgorithm


class FbvsTest:
    """
    This class contains tests for the algorithms
    """

    def __init__(self, algorithm: FeedbackVertexSetAlgorithm):
        self.algorithm = algorithm

    def test(self):
        # a graph with 2 cycles that can be broken by removing 1 node (node 0)
        print("Testing a custom graph", end="")
        graph = nx.Graph()
        graph.add_cycle([0,1,2,3])
        graph.add_cycle([0,3,4,5])
        fbvs = self.algorithm.get_fbvs(graph)
        assert len(fbvs) == 1
        print(" [Passed]")

        print("Testing a complete graph", end="")
        graph = nx.complete_graph(5)
        fbvs = self.algorithm.get_fbvs(graph)
        assert len(fbvs) == 3
        print(" [Passed]")

        print("Testing an acyclic graph (star)", end="")
        graph = nx.star_graph(7)
        fbvs = self.algorithm.get_fbvs(graph)
        assert len(fbvs) == 0
        print(" [Passed]")
