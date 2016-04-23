from algorithms.bruteforce import Bruteforce
from algorithms.bruteforce_cycle import BruteforceCycle
from algorithms.iterative_compression import IterativeCompression
from algorithms.maximum_induced_forest import MaximumInducedForest
from tools.utils import *


def fvs_via_mif(g: MultiGraph, k: int) -> set:
    mif = MaximumInducedForest()
    result = mif.get_fbvs(g)
    return result


def fvs_via_bruteforce(g: MultiGraph, k: int) -> set:
    bf = BruteforceCycle()
    gx = multigraph_to_graph(g)
    rx = bf.get_fbvs(gx)
    return rx


def fvs_via_dumb_bruteforce(g: MultiGraph, k: int) -> set:
    dbf = Bruteforce()
    gx = multigraph_to_graph(g)
    rx = dbf.get_fbvs(gx)
    return rx


def fvs_via_ic_opt(g: MultiGraph, k: int) -> set:
    ic = IterativeCompression()
    result = ic.get_fbvs(g)
    return result


def fvs_via_ic_dec(g: MultiGraph, k: int) -> set:
    ic = IterativeCompression()
    result = ic.get_fbvs_max_size(g, k)
    return result
