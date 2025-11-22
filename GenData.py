import numpy as np
import KAPS_DifferentDistributions
import KAPS_BaseAlgorithm




def gen_uniform(N, low=0, high=None, rng=None):
    if high is None:
        high = N*100

    return np.sort(np.random.uniform(low,N*100,N))

def gen_zipf(N, a=2.0, cap=10**12, rng=None):
    x = (rng or np.random).zipf(a, N)
    x = np.minimum(x, cap)
    return x