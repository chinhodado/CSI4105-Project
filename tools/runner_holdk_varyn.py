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

    we hold the value k as a constant and generate graphs with varying n
    we perform this experiment for k = 2,4,8

    results appear as algorithms in above order,
    algorithm: { graph size n : running time }

    """

    # generate data
    k = 2
    n = k+2
    count = 0
    data = dict()

    while count < 4:
        tg = generate_custom(k, 100)

        if len(tg) == n:
            print("graph generated graph with k = {}, n = {}.".format(k, len(tg)))
            data[n] = tg
            count = len(data)
            n*=2

    times_bruteforce = dict()
    times_bruteforce_cyc = dict()
    times_ic_opt = dict()
    times_mif = dict()

    for n, g in data.items():

        fvs, time = time_instance(MultiGraph(g), k, alg=fvs_via_dumb_bruteforce, n=1)
        print("bruteforce with k = {}, n = {}, time = {:.3f}.".format(len(fvs), len(g), time))
        times_bruteforce[n] = '{:.3f}'.format(time)

        fvs, time = time_instance(MultiGraph(g), k, alg=fvs_via_bruteforce, n=1)
        print("bruteforce_cyc with k = {}, n = {}, time = {:.3f}.".format(len(fvs), len(g), time))
        times_bruteforce_cyc[n] = '{:.3f}'.format(time)

        fvs, time = time_instance(MultiGraph(g), k, alg=fvs_via_ic_opt, n=1)
        print("ic_opt with k = {}, n = {}, time = {:.3f}.".format(len(fvs), len(g), time))
        times_ic_opt[n] = '{:.3f}'.format(time)

        fvs, time = time_instance(MultiGraph(g), k, alg=fvs_via_mif, n=1)
        print("mif with k = {}, n = {}, time = {:.3f}.".format(len(fvs), len(g), time))
        times_mif[n] = '{:.3f}'.format(time)

    print(times_bruteforce)
    print(times_bruteforce_cyc)
    print(times_ic_opt)
    print(times_mif)

if __name__ == "__main__":
    main()
