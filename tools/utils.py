import itertools
from networkx import Graph
from networkx import MultiGraph
from networkx.algorithms.tree import is_forest


def multigraph_to_graph(g: MultiGraph) -> Graph:
    gx = Graph()
    gt = Graph(g)
    gx.add_nodes_from(gt.nodes())
    gx.add_edges_from(gt.edges())
    return gx


def graph_to_multigraph(g: Graph) -> MultiGraph:
    gx = MultiGraph(g)
    return gx


# Original (unused) code for G - W.
def graph_minus_slow(g: MultiGraph, w: set) -> MultiGraph:
    gx = g.copy()
    gx.remove_nodes_from(w)
    return gx


# Optimised code for G - W (yields an approx 2x speed-up).
def graph_minus(g: MultiGraph, w: set) -> MultiGraph:
    gx = MultiGraph()
    for (n1, n2) in g.edges():
        if n1 not in w and n2 not in w:
            gx.add_edge(n1, n2)
    for n in g.nodes():
        if n not in w:
            gx.add_node(n)
    return gx


def is_fvs(g: MultiGraph, w) -> bool:
    h = graph_minus(g, w)
    return (len(h) == 0) or is_forest(h)


def is_independent_set(g: MultiGraph, f: set) -> bool:
    for edge in itertools.combinations(f, 2):
        if g.has_edge(edge[0], edge[1]):
            return False
    return True


def remove_node_deg_01(g: MultiGraph) -> bool:
    """
    Delete all vertices of degree 0 or 1 in a graph
    """
    changed = False
    for v in g.nodes():
        if g.degree(v) <= 1:
            g.remove_node(v)
            changed = True
    return changed
