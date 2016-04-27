import itertools

from networkx import Graph, cycle_basis

from algorithms.feedback_vertex_set_algorithm import FeedbackVertexSetAlgorithm
from tools.utils import remove_node_deg_01, graph_minus, is_acyclic


class BruteforceCycleSubset(FeedbackVertexSetAlgorithm):
    """
    A mix of Bruteforce and BruteforceCycle, where we just bruteforce those nodes in at least one cycle
    """

    def get_fbvs(self, graph: Graph):
        if is_acyclic(graph):
            return set()

        # remove all nodes of degree 0 or 1 as they can't be part of any cycles
        remove_node_deg_01(graph)

        # get the set of nodes that is in at least one cycle
        cycles = cycle_basis(graph)
        nodes_in_cycles = set([item for sublist in cycles for item in sublist])

        for L in range(0, len(nodes_in_cycles) + 1):
            for subset in itertools.combinations(nodes_in_cycles, L):
                # make an induced subgraph with the current node subset removed
                new_graph = graph_minus(graph, subset)

                if is_acyclic(new_graph):
                    return subset

        return set()

    def get_fbvs_max_size(self, graph: Graph, k: int) -> set:
        raise Exception("Undefined for this algorithm")