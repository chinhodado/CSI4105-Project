import sys

import networkx as nx
from networkx.algorithms.tree import is_forest

from algorithms.feedback_vertex_set_algorithm import FeedbackVertexSetAlgorithm
from tools.utils import remove_node_deg_01


class BruteforceCycle(FeedbackVertexSetAlgorithm):
    """
    A bruteforce algorithm to find the min size feedback vertex set
    This algorithm will find all nodes that belong to at least one cycle. For each of those nodes,
    it recursively run the algorithm on the induced subgraph with the node removed to find the min fbvs

    WARNING: THERE IS NO GUARANTEE THAT THIS ALGORITHM IS CORRECT!!! E.G. THERE'S NO GUARANTEE THAT THE
    RETURNED FBVS IS THE MINIMUM ONE!
    """

    def __init__(self):
        # a dict to hold previously-computed min fvbs
        # the key is a frozenset of nodes, and the value is the min fvbs of the subgraph induced on that set of nodes
        self.cacheDict = {}

    def get_fbvs(self, graph):
        if is_forest(graph):
            return set()

        # remove all nodes of degree 0 or 1 as they can't be part of any cycles
        remove_node_deg_01(graph)

        # reset the cache dict
        self.cacheDict = {}
        return self._get_fbvs(graph)

    def _get_fbvs(self, graph):
        # get the list of cycles
        cycles = nx.cycle_basis(graph)

        # if the graph is already acyclic, there's nothing to remove, so return an empty set
        if len(cycles) == 0:
            return set()

        # get the set of nodes that is in at least one cycle
        nodes_in_cycles = set([item for sublist in cycles for item in sublist])

        min_num_to_remove = sys.maxsize
        min_nodes_to_remove = set()

        for node in nodes_in_cycles:
            # make an induced subgraph with the current node removed
            nodes = graph.nodes()
            nodes.remove(node)
            nodes_set = frozenset(nodes)

            if nodes_set in self.cacheDict:
                # if we have previously calculated the min fbvs for this induced subgraph, get that
                # fbvs from the cache dict
                nodes_to_remove = self.cacheDict[nodes_set]
            else:
                # otherwise we have to calculate it
                new_graph = graph.subgraph(nodes)
                nodes_to_remove = self._get_fbvs(new_graph)

                # add the newly calculated fbvs to the cache dict
                self.cacheDict[nodes_set] = nodes_to_remove

            if len(nodes_to_remove) < min_num_to_remove:
                min_num_to_remove = len(nodes_to_remove)
                nodes_to_remove.add(node)
                min_nodes_to_remove = nodes_to_remove

        return min_nodes_to_remove

    def get_fbvs_max_size(self, graph, k) -> set:
        raise Exception("Undefined for this algorithm")
