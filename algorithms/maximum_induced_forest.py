from networkx import number_connected_components, connected_components, find_cycle

from algorithms.feedback_vertex_set_algorithm import FeedbackVertexSetAlgorithm
from tools.utils import *


class MaximumInducedForest(FeedbackVertexSetAlgorithm):
    """
    Maximum Induced Forest algorithm for the undirected feedback vertex set problem from chapter 6.2 of
    Exact Exponential Algorithms by Fomin, Fedor V., Kratsch, Dieter

    Instead of computing a minimum feedback vertex set directly, this algorithm finds the maximum size
    of an induced forest in a graph. In fact, it solves a more general problem: for any
    acyclic set F it finds the maximum size of an induced forest containing F.
    """

    def get_fbvs(self, graph: Graph):
        if is_forest(graph):
            return set()

        # Save the original node set for later use since we'll mutate the graph
        nodes = set(graph.nodes())

        if type(graph) is not MultiGraph:
            graph = MultiGraph(graph)

        mif_set = self.preprocess_1(graph, set(), None)
        if mif_set is not None:
            fbvs = nodes.difference(mif_set)
            return fbvs

        return None

    def get_fbvs_max_size(self, graph: Graph, k: int) -> set:
        raise Exception("Undefined for this algorithm")

    def preprocess_1(self, g: MultiGraph, f: set, active_v) -> set:
        if number_connected_components(g) >= 2:
            mif_set = set()
            for component in connected_components(g):
                f_i = component.intersection(f)
                gx = g.subgraph(component)
                component_mif_set = self.preprocess_2(gx, f_i, active_v)
                if component_mif_set:
                    mif_set = mif_set.union(component_mif_set)
            return mif_set
        return self.preprocess_2(g, f, active_v)

    def preprocess_2(self, g: MultiGraph, f: set, active_v) -> set:
        mif_set = set()
        while not is_independent_set(g, f):
            mif_set = mif_set.union(f)
            for component in connected_components(g.subgraph(f)):
                if len(component) > 1:
                    if active_v in component:
                        active_v = component.pop()
                        compressed_node = active_v
                    else:
                        compressed_node = component.pop()
                    g = self.compress(g, component, compressed_node, True)
                    f = f.intersection(g.nodes())
                    # Maybe faster with
                    # f = f.difference(component)
                    # f.add(compressed_node)
                    mif_set = mif_set.union(component)
                    break
        mif_set2 = self.mif_main(g, f, active_v)
        if mif_set2:
            mif_set = mif_set2.union(mif_set)

        return mif_set

    def compress(self, g: MultiGraph, t: set, compressed_node, mutate=False) -> MultiGraph:
        if not t:
            return g
        if mutate:
            gx = g
        else:
            gx = g.copy()

        tx = t
        if compressed_node in tx:
            tx = t.copy()
            tx.remove(compressed_node)
        gx.add_node(compressed_node)

        for node in tx:
            for edge in gx.edges(node):
                if edge[0] == node:
                    node_2 = edge[1]
                else:
                    node_2 = edge[0]
                if not (node_2 in t or node_2 == compressed_node):
                    gx.add_edge(compressed_node, node_2)
            gx.remove_node(node)

        remove = set()
        for node in gx.adj[compressed_node]:
            if len(gx.adj[compressed_node][node]) >= 2:
                # Using a set to remove to avoid messing up iteration of adj
                remove.add(node)

        for node in remove:
            gx.remove_node(node)

        return gx

    def generalized_degree(self, g: MultiGraph, f: set, active_node, node) -> (int, set):
        assert g.has_node(node), "Calculating gd for node which is not in g!"

        k = set(g.neighbors(node))
        k.remove(active_node)
        k = k.intersection(f)

        gx = self.compress(g, k, node)

        neighbors = gx.neighbors(node)
        neighbors.remove(active_node)

        return len(neighbors), neighbors

    def mif_main(self, g: MultiGraph, f: set, t) -> set:
        if f == g.nodes():
            return f
        if not f:
            g_degree = g.degree()
            g_max_degree_node = max(g_degree, key=lambda n: g_degree[n])
            if g_degree[g_max_degree_node] <= 1:
                return set(g.nodes())
            else:
                fx = f.copy()
                fx.add(g_max_degree_node)
                gx = g.copy()
                gx.remove_node(g_max_degree_node)
                mif_set1 = self.preprocess_1(g, fx, t)
                mif_set2 = self.preprocess_1(gx, f, t)
                if not mif_set1:
                    return mif_set2
                elif not mif_set2:
                    return mif_set1
                else:
                    return max(mif_set1, mif_set2, key=len)

        # Set t as active vertex
        if t is None or t not in f:
            t = next(iter(f))

        gd_over_3 = None
        gd_2 = None
        for v in g.neighbors_iter(t):
            (gd_v, gn_v) = self.generalized_degree(g, f, t, v)
            if gd_v <= 1:
                f.add(v)
                return self.preprocess_1(g, f, t)
            elif gd_v >= 3:
                gd_over_3 = v
            else:
                gd_2 = (v, gn_v)
        if gd_over_3 is not None:
            # Cannot simply use "if gd_over_3" because v might be 0
            fx = f.copy()
            fx.add(gd_over_3)
            gx = g.copy()
            gx.remove_node(gd_over_3)
            mif_set1 = self.preprocess_1(g, fx, t)
            mif_set2 = self.preprocess_1(gx, f, t)
            if not mif_set1:
                return mif_set2
            elif not mif_set2:
                return mif_set1
            else:
                return max(mif_set1, mif_set2, key=len)
        elif gd_2 is not None:
            (v, gn) = gd_2
            fx1 = f.copy()
            fx2 = f.copy()
            fx1.add(v)
            for n in gn:
                fx2.add(n)
            gx = g.copy()
            gx.remove_node(v)
            try:
                find_cycle(gx.subgraph(fx2))
                mif_set1 = None
            except:
                mif_set1 = self.preprocess_1(gx, fx2, t)
            mif_set2 = self.preprocess_1(g, fx1, t)
            if not mif_set1:
                return mif_set2
            elif not mif_set2:
                return mif_set1
            else:
                return max(mif_set1, mif_set2, key=len)
        return None
