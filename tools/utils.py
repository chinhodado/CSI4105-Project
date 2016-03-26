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


def graph_minus(g: Graph, s: set) -> Graph:
    new_nodes = [x for x in g.nodes() if x not in s]
    new_graph = g.subgraph(new_nodes)
    return new_graph


def is_fvs(g: MultiGraph, w) -> bool:
    h = graph_minus(g, w)
    return (len(h) == 0) or is_forest(h)


def is_independent_set(g: MultiGraph, f: set) -> bool:
    for edge in itertools.combinations(f, 2):
        if g.has_edge(edge[0], edge[1]):
            return False
    return True


def remove_node_deg_01(g: Graph) -> bool:
    """
    Delete all nodes of degree 0 or 1 in a graph
    Return `True` if the graph was modified and `False` otherwise
    """
    changed = False
    for v in g.nodes():
        if g.degree(v) <= 1:
            g.remove_node(v)
            changed = True
    return changed
