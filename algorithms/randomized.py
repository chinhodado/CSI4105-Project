from random import choice
from typing import List

from networkx import MultiGraph, Graph

from algorithms.feedback_vertex_set_algorithm import FeedbackVertexSetAlgorithm
from tools.utils import graph_minus, is_acyclic


class Randomized(FeedbackVertexSetAlgorithm):
    """
    Randomized algorithm for the undirected feedback vertex set problem from chapter 5.1 of Parameterized Algorithms,
    Cygan, M., Fomin, F.V., Kowalik, Ł., Lokshtanov, D., Marx, D., Pilipczuk, M., Pilipczuk, M., Saurabh, S.

    This algorithm will, given a feedback vertex set instance (G, k), in time (4^k)(n^O(1)) either reports a failure
    or finds a feedback vertex set in G of size at most k. Moreover, if the algorithm is given a yes-instance,
    it returns a solution with a constant probability.

    Originally designed for the decision version of the problem (via the get_fbvs_max_size() method), this algorithm
    can also be used to solve the optimization version (via the get_fbvs() method). However, be aware that this
    algorithm is VERY SLOW when used to solve the optimization problem.
    """

    def get_fbvs(self, graph: Graph):
        if is_acyclic(graph):
            return set()

        if type(graph) is not MultiGraph:
            graph = MultiGraph(graph)

        for i in range(1, graph.number_of_nodes()):
            result = self.get_fbvs_max_size(graph, i)
            if result is not None:
                return result  # in the worst case, result is n-2 nodes

    def get_fbvs_max_size(self, g: MultiGraph, k: int) -> set:
        # we will run the algorithm 4^k times
        n = 4 ** k
        for _ in range (1, n):
            # pass a copy of g, since we need a fresh copy of g for every run
            sol = self._get_fbvs_max_size(g.copy(), k)
            if sol is not None:
                # we found a fbvs for (g,k), so we can return it right away
                return sol
        return None

    def _get_fbvs_max_size(self, g: MultiGraph, k: int) -> set:
        # Exhaustively apply reductions
        k, x0 = self.apply_reductions(g, k)

        # Originally reduction 5: if k < 0, terminate the algorithm and conclude that
        # (G, k) is a no-instance.
        if k < 0:
            return None

        # If G is an empty graph, then we return soln_redux
        if len(g) == 0:
            return x0

        # Pick a random edge, then a random end node of that edge
        rand_edge = choice(g.edges())
        v = choice(rand_edge)

        # We recurse on (G - v, k − 1).
        xn = self._get_fbvs_max_size(graph_minus(g, {v}), k - 1)

        if xn is None:
            # If the recursive step returns a failure, then we return a failure as well.
            return None
        else:
            # If the recursive step returns a feedback vertex set Xn, then we return X = Xn ∪ {v} ∪ X0.
            return xn.union({v}).union(x0)

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

    def reduction2(self, g: MultiGraph, k: int) -> (int, List[int], bool):
        """
        If there is an edge of multiplicity larger than 2, reduce its multiplicity to 2.

        Note: this reduction is not used. Instead of using this reduction, we instead make sure that in
        reduction 4, when we remove a node with degree 2, only create a new edge between the two
        neighbors of that node if there are currently less than two edges between those two neighbor nodes.
        """
        pass

    def reduction3(self, g: MultiGraph, k: int) -> (int, List[int], bool):
        """
        If there is a vertex v of degree at most 1, delete v.
        """
        changed = False
        for v in g.nodes():
            if g.degree(v) <= 1:
                g.remove_node(v)
                changed = True
        return k, None, changed

    def reduction4(self, g: MultiGraph, k: int) -> (int, List[int], bool):
        """
         If there is a vertex v of degree 2, delete v and connect its two neighbors by a new edge.
        """
        for v in g.nodes():
            if g.degree(v) == 2:
                # Delete v and make its neighbors adjacent.
                ne = g.neighbors(v)

                # We must check whether v has 2 neighbors, or just one but connected to v by multiple edges
                if len(ne) == 2:
                    [n1, n2] = ne
                else:
                    [n1] = ne
                    n2 = n1
                g.remove_node(v)

                # Only add the edge if there are currently less than 2 edges between these two nodes
                es = g[n1].get(n2, {})
                if len(es) < 2:
                    g.add_edge(n1, n2)
                return k, None, True
        return k, None, False

    def apply_reductions(self, g: MultiGraph, k: int) -> (int, set):
        """
        Exhaustively apply reductions.

        Note: reduction 5 has been moved directly into the body of the algorithm (_get_fbvs_max_size())
        """

        # Set of nodes included in the solution as a result of reductions.
        x = set()
        while True:
            reduction_applied = False
            # Note that only reduction1 can modify k (decrease it)
            # Also, only reduction1 can return a non-None x0
            for f in [self.reduction1, self.reduction3, self.reduction4]:
                (k, x0, changed) = f(g, k)

                if changed:
                    reduction_applied = True
                    if x0 is not None:
                        x = x.union(x0)

            if not reduction_applied:
                return k, x
