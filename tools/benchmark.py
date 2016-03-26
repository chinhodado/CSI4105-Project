import time
import multiprocessing as mp

from multiprocessing import Pool

from networkx import MultiGraph

TEN_MINUTES = 10 * 60  # seconds


def time_instance(g: MultiGraph, k: int, alg, n=1) -> (set, float):
    """
    Solve the given instance and return the time required to do so.
    """
    start = time.process_time()
    for _ in range(0, n):
        fvs = alg(g, k)
    end = time.process_time()
    return (fvs, (end - start) / n)


def time_all(graphs, alg) -> list:
    """
    Time a list of instances, waiting at most 10m for any single instance.
    If an instance times out, its result is `None`.

    :param graphs: [(MultiGraph, int)]
    :returns: [(fvs, time in seconds)]
    """
    with Pool(1) as p:
        results = []
        for (g, k) in graphs:
            promise = p.apply_async(func=time_instance, args=(g, k, alg))
            try:
                t = promise.get(TEN_MINUTES)
                results.append(t)
                print('.', flush=True, end='')
            except mp.TimeoutError:
                results.append(None)
                print('x', flush=True, end='')

        print("")
        return results
