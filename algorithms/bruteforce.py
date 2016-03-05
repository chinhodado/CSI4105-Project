import sys

import networkx as nx

from algorithms.feedback_vertex_set_algorithm import FeedbackVertexSetAlgorithm


class Bruteforce(FeedbackVertexSetAlgorithm):
    """
    A bruteforce algorithm to find the min size feedback vertex set
    This algorithm will find all nodes that belong to at least one cycle. For each of those nodes,
    it recursively run the algorithm on the induced subgraph with the node removed to find the min fbvs
    
    WARNING: THERE IS NO GUARANTEE THAT THIS ALGORITHM IS CORRECT!!! E.G. THERE'S NO GUARANTEE THAT THE
    RETURNED FBVS IS THE MINIMUM ONE!
    """

    def get_fbvs(self, graph):
        # get the list of cycles
        cycles = nx.cycle_basis(graph)

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
            new_graph = graph.subgraph(nodes)

            nodes_to_remove = self.get_fbvs(new_graph)

            if len(nodes_to_remove) < min_num_to_remove:
                min_num_to_remove = len(nodes_to_remove)
                nodes_to_remove.add(node)
                min_nodes_to_remove = nodes_to_remove

        return min_nodes_to_remove