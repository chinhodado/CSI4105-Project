import itertools

from networkx import MultiGraph, Graph
from networkx.algorithms.tree import is_forest

from algorithms.feedback_vertex_set_algorithm import FeedbackVertexSetAlgorithm
from tools.utils import graph_minus


class IterativeCompression(FeedbackVertexSetAlgorithm):
    """
    Iterative compression from Parametrzed Algorithms 4.3.1
    """

    def get_fbvs(self, graph: MultiGraph):
        if is_forest(graph):
            return set()

        for i in range(1, graph.number_of_nodes()):
            result = self.get_fbvs_max_size(graph, i)
            if result is not None:
                return result  # in the worst case, result is n-2 nodes

    def get_fbvs_max_size(self, g: MultiGraph, k: int) -> set:
        if len(g) <= k + 2:
            return set(g.nodes()[:k])

        # Construct a trivial FVS of size k + 1 on the first k + 3 vertices of G.
        nodes = g.nodes()

        # The set of nodes currently under consideration.
        node_set = set(nodes[:(k + 2)])

        # The current best solution, of size (k + 1) before each compression step,
        # and size <= k at the end.
        soln = set(nodes[:k])

        for i in range(k + 2, len(nodes)):
            soln.add(nodes[i])
            node_set.add(nodes[i])

            if len(soln) < k + 1:
                continue

            assert (len(soln) == (k + 1))
            assert (len(node_set) == (i + 1))

            new_soln = IterativeCompression.ic_compression(g.subgraph(node_set), soln, k)

            if new_soln is None:
                return None

            soln = new_soln
            assert (len(soln) <= k)

        return soln

    @staticmethod
    def reduction1(g: MultiGraph, w: set, h: MultiGraph, k: int) -> (int, int, bool):
        """
        Delete all nodes of degree 0 or 1 as they can't be part of any cycles.
        """
        changed = False
        for v in g.nodes():
            if g.degree(v) <= 1:
                g.remove_node(v)
                h.remove_nodes_from([v])
                changed = True
        return k, None, changed

    @staticmethod
    def reduction2(g: MultiGraph, w: set, h: MultiGraph, k: int) -> (int, int, bool):
        """
        If there exists a node v in H such that G[W ∪ {v}]
        contains a cycle, then include v in the solution, delete v and decrease the
        parameter by 1. That is, the new instance is (G - {v}, W, k - 1).

        If v introduces a cycle, it must be part of X as none of the vertices in W
        will be available to neutralise this cycle.
        """
        for v in h.nodes():
            # Check if G[W ∪ {v}] contains a cycle.
            if not is_forest(g.subgraph(w.union({v}))):
                g.remove_node(v)
                h.remove_nodes_from([v])
                return k - 1, v, True
        return k, None, False

    @staticmethod
    def reduction3(g: MultiGraph, w: set, h: MultiGraph, k: int) -> (int, int, bool):
        """
        If there is a node v ∈ V(H) of degree 2 in G such
        that at least one neighbor of v in G is from V (H), then delete this node
        and make its neighbors adjacent (even if they were adjacent before; the graph
        could become a multigraph now).
        """
        for v in h.nodes():
            if g.degree(v) == 2:
                # If v has a neighbour in H, short-curcuit it.
                if len(h[v]) >= 1:
                    # Delete v and make its neighbors adjacent.
                    [n1, n2] = g.neighbors(v)
                    g.remove_node(v)
                    g.add_edge(n1, n2)
                    # Update H accordingly.
                    h.remove_nodes_from([v])
                    if n1 not in w and n2 not in w:
                        h.add_edge(n1, n2)
                    return k, None, True
        return k, None, False

    @staticmethod
    def apply_reductions(g: MultiGraph, w: set, k: int) -> (int, set):
        """
        Exhaustively apply reductions. The three reductions are:

        Reduction 1: Delete all the nodes of degree at most 1 in G.

        Reduction 2: If there exists a node v in H such that G[W ∪ {v}]
            contains a cycle, then include v in the solution, delete v and decrease the
            parameter by 1. That is, the new instance is (G - {v}, W, k - 1).

        Reduction 3: If there is a node v ∈ V(H) of degree 2 in G such
            that at least one neighbor of v in G is from V(H), then delete this node
            and make its neighbors adjacent (even if they were adjacent before; the graph
            could become a multigraph now).
        """
        # Current H.
        h = graph_minus(g, w)

        # Set of nodes included in the solution as a result of reductions.
        x = set()
        while True:
            reduction_applied = False
            for f in [IterativeCompression.reduction1, IterativeCompression.reduction2,
                      IterativeCompression.reduction3]:
                (k, solx, changed) = f(g, w, h, k)

                if changed:
                    reduction_applied = True
                    if solx is not None:
                        x.add(solx)

            if not reduction_applied:
                return k, x

    @staticmethod
    def fvs_disjoint(g: MultiGraph, w: set, k: int) -> set:
        """
        Given an undirected graph G and a fbvs W in G of size at least (k + 1), is it possible to construct
        a fbvs X of size at most k using only the nodes of G - W?

        :return: The set X, or `None` if it's not possible to construct X
        """

        # If G[W] isn't a forest, then a solution X not using W can't remove W's cycles.
        if not is_forest(g.subgraph(w)):
            return None

        # Apply reductions exhaustively.
        k, soln_redux = IterativeCompression.apply_reductions(g, w, k)

        # If k becomes negative, it indicates that the reductions included
        # more than k nodes. In other word, reduction 2 shows that there are more than k nodes
        # in G - W that will create cycle in W. Hence, no solution of size <= k exists.
        if k < 0:
            return None

        # From now onwards we assume that k >= 0

        # If G has been reduced to nothing and k is >= 0 then the solution generated by the reductions
        # is already optimal.
        if len(g) == 0:
            return soln_redux

        # Recall that H is a forest as W is a feedback vertex set. Thus H has a node x of degree at most 1.
        # Find an x in H of degree at most 1.
        h = graph_minus(g, w)
        x = None
        for v in h.nodes():
            if h.degree(v) <= 1:
                x = v
                break
        assert x is not None, "There must be at least one node x of degree at most 1"

        # Branch on (G - {x}, W, k−1) and (G, W ∪ {x}, k)
        # G is copied in the left branch (as it is modified), but passed directly in the right.
        soln_left = IterativeCompression.fvs_disjoint(graph_minus(g, {x}), w, k - 1)

        if soln_left is not None:
            return soln_redux.union(soln_left).union({x})

        soln_right = IterativeCompression.fvs_disjoint(g, w.union({x}), k)

        if soln_right is not None:
            return soln_redux.union(soln_right)

        return None

    @staticmethod
    def ic_compression(g: MultiGraph, z: set, k: int) -> MultiGraph:
        """
        Given a graph G and an FVS Z of size (k + 1), construct an FVS of size at most k.
        Return `None` if no such solution exists.
        """
        assert (len(z) == k + 1)
        # i in {0 .. k}
        for i in range(0, k + 1):
            for xz in itertools.combinations(z, i):
                x = IterativeCompression.fvs_disjoint(graph_minus(g, xz), z.difference(xz), k - i)
                if x is not None:
                    return x.union(xz)
        return None
