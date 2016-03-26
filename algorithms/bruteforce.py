import itertools

from networkx.algorithms.tree import is_forest

from algorithms.feedback_vertex_set_algorithm import FeedbackVertexSetAlgorithm
from tools.utils import remove_node_deg_01


class Bruteforce(FeedbackVertexSetAlgorithm):
    """
    Bruteforce to find the min size feedback vertex set
    A true, dumb bruteforce that will guarantee to find the min fbvs
    Just try all combinations of nodes in the graph, for each combination check if the induced
    subgraph is acyclic
    This takes no consideration whether a node is in a cycle or not
    """

    def get_fbvs(self, graph):
        if is_forest(graph):
            return set()

        # remove all nodes of degree 0 or 1 as they can't be part of any cycles
        remove_node_deg_01(graph)

        nodes = graph.nodes()
        for L in range(0, len(nodes) + 1):
            for subset in itertools.combinations(nodes, L):
                # make an induced subgraph with the current node removed
                new_nodes = [x for x in graph.nodes() if x not in subset]
                new_graph = graph.subgraph(new_nodes)

                if is_forest(new_graph):
                    return subset

        return set()

    def get_fbvs_max_size(self, graph, k) -> set:
        raise Exception("Undefined for this algorithm")
