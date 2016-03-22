import itertools

import networkx.algorithms.components.connected as nxc
import networkx.algorithms.cycles as cyc
from networkx.algorithms.tree import is_forest

from algorithms.bruteforce import Bruteforce
from algorithms.dumb_bruteforce import DumbBruteforce
from algorithms.iterative_compression import IterativeCompression
from tools.utils import *


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


def compress(g: MultiGraph, t: set, compressed_node, mutate=False) -> MultiGraph:
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


def generalized_degree(g: MultiGraph, f: set, active_node, node) -> (int, set):
    assert g.has_node(node), "Calculating gd for node which is not in g!"

    k = set(g.neighbors(node))
    k.remove(active_node)
    k = k.intersection(f)

    gx = compress(g, k, node)

    neighbors = gx.neighbors(node)
    neighbors.remove(active_node)

    return len(neighbors), neighbors


def mif_main(g: MultiGraph, f: set, t, k: int) -> set:
    k_set = k is not None
    new_k1 = new_k2 = None
    if k_set and k > g.order():
        return None
    if f == g.nodes() or (k_set and k <= 0):
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
            if k_set:
                new_k1 = k - 1
                new_k2 = k
            mif_set1 = mif_preprocess_1(g, fx, t, new_k1)
            mif_set2 = mif_preprocess_1(gx, f, t, new_k2)
            if not mif_set1:
                return mif_set2
            elif not mif_set2:
                return mif_set1
            else:
                return max(mif_set1, mif_set2, key=len)

    # Set t as active vertex
    if t is None or not t in f:
        t = next(iter(f))

    gd_over_3 = None
    gd_2 = None
    for v in g.neighbors_iter(t):
        (gd_v, gn_v) = generalized_degree(g, f, t, v)
        if gd_v <= 1:
            f.add(v)
            if k_set:
                new_k1 = k - 1
            return mif_preprocess_1(g, f, t, new_k1)
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
        if k_set:
            new_k1 = k - 1
            new_k2 = k
        mif_set1 = mif_preprocess_1(g, fx, t, new_k1)
        mif_set2 = mif_preprocess_1(gx, f, t, new_k2)
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
        if k_set:
            new_k1 = k - 2
            new_k2 = k - 1
        try:
            cyc.find_cycle(gx.subgraph(fx2))
            mif_set1 = None
        except:
            mif_set1 = mif_preprocess_1(gx, fx2, t, new_k1)
        mif_set2 = mif_preprocess_1(g, fx1, t, new_k2)
        if not mif_set1:
            return mif_set2
        elif not mif_set2:
            return mif_set1
        else:
            return max(mif_set1, mif_set2, key=len)
    return None


def mif_preprocess_2(g: MultiGraph, f: set, active_v, k: int) -> set:
    mif_set = set()
    while not is_independent_set(g, f):
        mif_set = mif_set.union(f)
        for component in nxc.connected_components(g.subgraph(f)):
            if len(component) > 1:
                if active_v in component:
                    active_v = component.pop()
                    compressed_node = active_v
                else:
                    compressed_node = component.pop()
                g = compress(g, component, compressed_node, True)
                f = f.intersection(g.nodes())
                # Maybe faster with
                # f = f.difference(component)
                # f.add(compressed_node)
                mif_set = mif_set.union(component)
                break
    mif_set2 = mif_main(g, f, active_v, k)
    if mif_set2:
        mif_set = mif_set2.union(mif_set)
    if k is None or len(mif_set) >= k:
        return mif_set
    return None


def mif_preprocess_1(g: MultiGraph, f: set, active_v, k: int) -> set:
    if nxc.number_connected_components(g) >= 2:
        mif_set = set()
        for component in nxc.connected_components(g):
            f_i = component.intersection(f)
            gx = g.subgraph(component)
            component_mif_set = mif_preprocess_2(gx, f_i, active_v, None)
            if component_mif_set:
                mif_set = mif_set.union(component_mif_set)
                if k is not None:
                    k -= (len(component_mif_set) - len(f_i))
                    if k <= 0:
                        return mif_set
        if k is None or len(mif_set) >= k:
            return mif_set
        return None
    return mif_preprocess_2(g, f, active_v, k)


def mif(g: MultiGraph, k=None) -> set:
    mif_set = mif_preprocess_1(g, set(), None, k)
    if k is not None and mif_set:
        if len(mif_set) < k:
            mif_set = None
    return mif_set


def fvs_via_mif(g: MultiGraph, k: int) -> set:
    mif_set = mif(g, g.order() - k)
    if mif_set:
        nodes = set(g.nodes())
        mif_set = nodes.difference(mif_set)
    return mif_set


def fvs_via_bruteforce(g: MultiGraph, k: int) -> set:
    bf = Bruteforce()
    gx = multigraph_to_graph(g)
    rx = bf.get_fbvs(gx)
    return rx


def fvs_via_dumb_bruteforce(g: MultiGraph, k: int) -> set:
    dbf = DumbBruteforce()
    gx = multigraph_to_graph(g)
    rx = dbf.get_fbvs(gx)
    return rx

def fvs_via_ic_opt(g: MultiGraph, k: int) -> set:
    ic = IterativeCompression()
    result = ic.get_fbvs(g)
    return result

def fvs_via_ic2_dec(g: MultiGraph, k: int) -> set:
    ic = IterativeCompression()
    result = ic.get_fbvs_max_size(g, k)
    return result