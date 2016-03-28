import itertools
from random import choice
from typing import List

from networkx import MultiGraph, Graph
from networkx.algorithms.tree import is_forest

from algorithms.feedback_vertex_set_algorithm import FeedbackVertexSetAlgorithm
from tools.utils import graph_minus


class Randomized(FeedbackVertexSetAlgorithm):
    """
    Randomized algorithm from Parametrzed Algorithms 5.1
    """

    def get_fbvs(self, graph: Graph):
        if is_forest(graph):
            return set()

        if type(graph) is not MultiGraph:
            graph = MultiGraph(graph)

        for i in range(1, graph.number_of_nodes()):
            result = self.get_fbvs_max_size(graph, i)
            if result is not None:
                return result  # in the worst case, result is n-2 nodes

    def get_fbvs_max_size(self, g: MultiGraph, k: int) -> set:
        n = 4 ** k
        for _ in range (1, n):
            sol = self._get_fbvs_max_size(g.copy(), k)
            if sol is not None:
                return sol
        return None

    def _get_fbvs_max_size(self, g: MultiGraph, k: int) -> set:
        k, soln_redux = self.apply_reductions(g, k)

        if k < 0:
            return None

        if len(g) == 0:
            return soln_redux

        # get random edge, then a random node
        rand_edge = choice(g.edges())
        v = choice(rand_edge)

        xn = self._get_fbvs_max_size(graph_minus(g, {v}), k - 1)

        if xn is None:
            return None
        else:
            return xn.union({v}).union(soln_redux)

    def reduction1(self, g: MultiGraph, k: int) -> (int, List[int], bool):
        """
        If there is a loop at a vertex v, delete v from the graph and decrease k by 1.
        """
        changed = False
        vs = g.nodes_with_selfloops()
        for v in vs:
            g.remove_node(v)
            k -= 1
            changed = True
        return k, vs, changed

    def reduction2(self, g: MultiGraph, k: int) -> (int, int, bool):
        """
        If there is an edge of multiplicity larger than 2, reduce its multiplicity to 2.
        """
        pass

    def reduction3(self, g: MultiGraph, k: int) -> (int, int, bool):
        """
        If there is a vertex v of degree at most 1, delete v.
        """
        changed = False
        for v in g.nodes():
            if g.degree(v) <= 1:
                g.remove_node(v)
                changed = True
        return k, None, changed

    def reduction4(self, g: MultiGraph, k: int) -> (int, int, bool):
        """
         If there is a vertex v of degree 2, delete v and connect its two neighbors by a new edge.
        """
        for v in g.nodes():
            if g.degree(v) == 2:
                # Delete v and make its neighbors adjacent.
                ne = g.neighbors(v)
                if len(ne) == 2:
                    [n1, n2] = ne
                else:
                    [n1] = ne
                    n2 = n1
                g.remove_node(v)

                # only add edge if the multiplicity is less than 2
                es = g[n1].get(n2, {})
                if len(es) < 2:
                    g.add_edge(n1, n2)
                return k, None, True
        return k, None, False

    def apply_reductions(self, g: MultiGraph, k: int) -> (int, set):
        """
        Exhaustively apply reductions.
        """

        # Set of nodes included in the solution as a result of reductions.
        x = set()
        while True:
            reduction_applied = False
            for f in [self.reduction1, self.reduction3, self.reduction4]:
                (k, solx, changed) = f(g, k)

                if changed:
                    reduction_applied = True
                    if solx is not None:
                        x = x.union(solx)

            if not reduction_applied:
                return k, x
