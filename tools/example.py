# Generate and solve a random instance using the iterative compression algorithm.

from algorithms.fvs import *
from tools.benchmark import *
from tools.generate import *


def main():
    k = 5
    cg = generate_random_graph(k)
    # cg = generate_complete_graph(k)

    print("\n --- example.py --- ")

    print("Graph parameters:\n")
    print("|V| = {}\n".format(len(cg)))
    print("E = {}\n".format(cg.edges()))
    print("|E| = {}\n".format(len(cg.edges())))

    print("\nAlgorithm: iterative compression with k = {}.".format(k))
    fvs, time = time_instance(cg, k, alg=fvs_via_ic, n=1)
    print("Done!")
    print("FVS = {} with size {}.".format(fvs, len(fvs)))
    print("Computation took {:.3f} seconds.".format(time))

    print("\nAlgorithm: dumb brute force with k = {}.".format(k))
    fvs2, time2 = time_instance(cg, k, alg=fvs_via_dumb_bruteforce, n=1)
    print("Done!")
    print("FVS = {} with size {}.".format(fvs2, len(fvs2)))
    print("Computation took {:.3f} seconds.".format(time2))

    print("\nAlgorithm: brute force with k = {}.".format(k))
    fvs3, time3 = time_instance(cg, k, alg=fvs_via_bruteforce, n=1)
    print("Done!")
    print("FVS = {} with size {}.".format(fvs3, len(fvs3)))
    print("Computation took {:.3f} seconds.".format(time3))

    print("\n --- example.py --- ")

if __name__ == "__main__":
    main()
