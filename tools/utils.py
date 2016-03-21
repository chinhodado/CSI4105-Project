from networkx import Graph
from networkx import MultiGraph


def multigraph_to_graph(g: MultiGraph) -> Graph:
    gx = Graph()
    gt = Graph(g)
    gx.add_nodes_from(gt.nodes())
    gx.add_edges_from(gt.edges())
    return gx


def graph_to_multigraph(g: Graph) -> MultiGraph:
    gx = MultiGraph(g)
    return gx
