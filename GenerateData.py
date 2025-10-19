import numpy as np
import KAPS_DifferentDistributions
import time

# -----------------------------
# Distributions
# -----------------------------
def gen_uniform(N, low=0, high=10**9, rng=None):
    return (rng or np.random).integers(low, high, size=N, dtype=np.int64)

def gen_zipf(N, a=2.0, cap=10**12, rng=None):
    x = (rng or np.random).zipf(a, N)
    x = np.minimum(x, cap)
    return x.astype(np.int64)

def gen_exponential(N, scale=1e4, rng=None):
    x = (rng or np.random).exponential(scale, N)
    x = x**2
    return x.astype(np.int64)

def gen_clustered(N, clusters=5, spread=10000, max_base=10**9, rng=None):
    rng = rng or np.random
    centers = np.linspace(0, max_base, clusters, dtype=np.int64)
    sizes = np.full(clusters, N // clusters, dtype=int)
    sizes[: (N % clusters)] += 1
    parts = []
    for c, sz in zip(centers, sizes):
        low = max(0, c - spread // 2)
        high = min(max_base, c + spread // 2 + 1)
        parts.append(rng.integers(low, high, size=sz, dtype=np.int64))
    return np.concatenate(parts)

def gen_near_uniform(N, hot_frac=0.1, hot_low=10**6, hot_high=10**6 + 5000,
                     base_low=0, base_high=10**9, rng=None):
    rng = rng or np.random
    k_hot = int(N * hot_frac)
    base = rng.integers(base_low, base_high, size=N, dtype=np.int64)
    if k_hot > 0:
        base[:k_hot] = rng.integers(hot_low, hot_high, size=k_hot, dtype=np.int64)
    return base

DIST_FUNCS = {
    "uniform": gen_uniform,
    "zipf": gen_zipf,
    "exponential": gen_exponential,
    "clustered": gen_clustered,
    "near_uniform": gen_near_uniform,
}

# -----------------------------
# Generate into arr
# -----------------------------
def generate_array(N, dist="uniform", seed=None):
    rng = np.random.default_rng(seed) if seed is not None else np.random.default_rng()
    if dist not in DIST_FUNCS:
        raise ValueError(f"Unknown distribution '{dist}'. Options: {list(DIST_FUNCS)}")

    # generate more than needed, then remove duplicates
    raw_values = DIST_FUNCS[dist](N * 2, rng=rng)  # oversample
    unique_values = np.unique(raw_values)

    # if we still don’t have enough uniques, fall back to random.choice without replacement
    if len(unique_values) < N:
        # just pick N unique values in the allowed range
        low, high = 0, 10**9
        unique_values = rng.choice(np.arange(low, high, dtype=np.int64), size=N, replace=False)
    else:
        unique_values = unique_values[:N]

    unique_values.sort(kind="mergesort")
    arr = unique_values.astype(int).tolist()
    return arr



# -----------------------------
# Example usage
# -----------------------------
if __name__ == "__main__":
    arr = generate_array(1000000, dist="exponential", seed=176886)



    import matplotlib.pyplot as plt

    plt.plot(arr)
    #plt.show()

    depths = [0,0,0,0,0]

    positionsInArray = [0.1,0.3,0.5,0.7,0.9,1.3,1.8,2.5,3.5,5,7,10,15,20,25,30,40,50,60,70,75,80,85,90,92,95,97,98,99,99.5,99.8,99.9]

    for j in positionsInArray:

        target = arr[int(j*len(arr)/100)]

        depth1, depth2, depth3, depth4, depth5 = 0,0,0,0,0

        for i in [2,4,8,16,32,64]:

            output1 = KAPS_DifferentDistributions.kaps(0, len(arr)-1, arr, target, i, 2, KAPS_DifferentDistributions.G_exponential(lmbda=0.00000005))
            output2 = KAPS_DifferentDistributions.kaps(0, len(arr)-1, arr, target, i, 2, KAPS_DifferentDistributions.G_exponential(lmbda=0.00000001))
            output3 = KAPS_DifferentDistributions.kaps(0, len(arr)-1, arr, target, i, 2, KAPS_DifferentDistributions.G_uniform())
            output4 = KAPS_DifferentDistributions.kaps(0, len(arr)-1, arr, target, i, 2, KAPS_DifferentDistributions.G_zipf_log())
            output5 = KAPS_DifferentDistributions.kaps(0, len(arr)-1, arr, target, i, 2, KAPS_DifferentDistributions.G_weibull(.5, 10**8))

            depth1 += output1[1]
            depth2 += output2[1]
            depth3 += output3[1]
            depth4 += output4[1]
            depth5 += output5[1]

            #print(f"Output {i}: {output_[0]}, depth: {output_[1]}")
            #print(f"Output {i}: {output2[0]}, depth: {output2[1]}")
            #print(f"Output {i}: {output3[0]}, depth: {output3[1]}")
            #print("-"*40)

        #print("+="*30)
        print(depth1, depth2, depth3, depth4, depth5)

        depths[0] += depth1
        depths[1] += depth2
        depths[2] += depth3
        depths[3] += depth4
        depths[4] += depth5
        print("+="*30)

    print(depths)

#output = thingy(0, len(arr)-1, arr, 687, 10, 2)