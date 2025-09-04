import numpy as np

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
    values = DIST_FUNCS[dist](N, rng=rng)
    values.sort(kind="mergesort")  # keep sorted
    # build arr = [[index, value], ...]
    arr = [[i, int(v)] for i, v in enumerate(values)]
    return arr

# -----------------------------
# Example usage
# -----------------------------
if __name__ == "__main__":
    arr = generate_array(10**5, dist="zipf", seed=42)
    print(f"✅ Generated arr with {len(arr):,} rows (first 5):")
    print(arr[:5])
