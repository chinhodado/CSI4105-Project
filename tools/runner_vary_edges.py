from algorithms.fvs import *
from tools.benchmark import *
from tools.generate import *


def main():

    """
    list of algos:
    fvs_via_dumb_bruteforce
    fvs_via_bruteforce (cycle)
    fvs_via_ic_opt
    fvs_via_mif

    we apply the algorithms to graphs as we vary the density of the graphs
    by varying the probability of edge creation with 0.25, 0.5, and 0.75

    results appear as algorithms in above order,
    algorithm: { fbvs size k : running time }

    """

    # generate data
    data = dict()
    k = 4

    while k < 513:
        tg = nx.erdos_renyi_graph(k, 0.25)
        data[k] = tg
        k*=2

    times_bruteforce = dict()
    times_bruteforce_cyc = dict()
    times_ic_opt = dict()
    times_mif = dict()

    for k, g in data.items():

        fvs, time = time_instance(MultiGraph(g), k, alg=fvs_via_dumb_bruteforce, n=1)
        print("bruteforce with k = {}, n = {}, time = {:.3f}.".format(len(fvs), len(g), time))
        times_bruteforce[k] = '{:.3f}'.format(time)

        fvs, time = time_instance(MultiGraph(g), k, alg=fvs_via_bruteforce, n=1)
        print("bruteforce_cyc with k = {}, n = {}, time = {:.3f}.".format(len(fvs), len(g), time))
        times_bruteforce_cyc[k] = '{:.3f}'.format(time)

        fvs, time = time_instance(MultiGraph(g), k, alg=fvs_via_ic_opt, n=1)
        print("ic_opt with k = {}, n = {}, time = {:.3f}.".format(len(fvs), len(g), time))
        times_ic_opt[k] = '{:.3f}'.format(time)

        fvs, time = time_instance(MultiGraph(g), k, alg=fvs_via_mif, n=1)
        print("mif with k = {}, n = {}, time = {:.3f}.".format(len(fvs), len(g), time))
        times_mif[k] = '{:.3f}'.format(time)

    print(times_bruteforce)
    print(times_bruteforce_cyc)
    print(times_ic_opt)
    print(times_mif)

if __name__ == "__main__":
    main()
