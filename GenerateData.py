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

def gen_exponential(N, scale=1e6, rng=None):
    x = (rng or np.random).exponential(scale, N)
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
    arr = generate_array(10**6, dist="exponential", seed=15)

    t_start = time.perf_counter_ns()
    output1 = KAPS_DifferentDistributions.kaps(0, len(arr)-1, arr, 870479, 100, 2, KAPS_DifferentDistributions.G_uniform())
    output2 = KAPS_DifferentDistributions.kaps(0, len(arr)-1, arr, 870479, 10, 2, KAPS_DifferentDistributions.G_uniform())
    output3 = KAPS_DifferentDistributions.kaps(0, len(arr)-1, arr, 870479, 10, 2, KAPS_DifferentDistributions.G_exponential(lmbda=0.001))
    output4 = KAPS_DifferentDistributions.kaps(0, len(arr)-1, arr, 870479, 10, 2, KAPS_DifferentDistributions.G_exponential(lmbda=0.0000001))
    output5 = KAPS_DifferentDistributions.kaps(0, len(arr)-1, arr, 870479, 25, 5, KAPS_DifferentDistributions.G_exponential(lmbda=0.0000001))
    output6 = KAPS_DifferentDistributions.kaps(0, len(arr)-1, arr, 870479, 25, 5, KAPS_DifferentDistributions.G_exponential(lmbda=0.000001))
    output7 = KAPS_DifferentDistributions.kaps(0, len(arr)-1, arr, 870479, 10, 2, KAPS_DifferentDistributions.G_exponential(lmbda=0.000001))
    t_end = time.perf_counter_ns()

    elapsed_ns = t_end - t_start
    elapsed_s = elapsed_ns / 1e9
    elapsed_us = elapsed_ns / 1e3

    print(f"Elapsed: {elapsed_s:.9f} s ({elapsed_us:.2f} µs)")
    print(f"Output: {output1[0]}, depth: {output1[1]}")
    print(f"Output: {output2[0]}, depth: {output2[1]}")
    print(f"Output: {output3[0]}, depth: {output3[1]}")
    print(f"Output: {output4[0]}, depth: {output4[1]}")
    print(f"Output: {output5[0]}, depth: {output5[1]}")
    print(f"Output: {output6[0]}, depth: {output6[1]}")
    print(f"Output: {output7[0]}, depth: {output7[1]}")

#output = thingy(0, len(arr)-1, arr, 687, 10, 2)