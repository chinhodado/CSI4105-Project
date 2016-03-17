
import networkx as nx

from bruteforce import Bruteforce

def main():
    bf = Bruteforce()
    k = 8

    cg = nx.complete_graph(k+2)
    mg = nx.MultiGraph()
    mg.add_nodes_from(cg.nodes())
    mg.add_edges_from(cg.edges())

    print("Algorithm: brute force with k = {}.".format(k))
    fvs = bf.get_fbvs(mg)
    print("\nDone!")
    print("FVS = {} with size {}.".format(fvs, len(fvs)))


if __name__=='__main__':
    main()


