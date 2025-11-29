import KAPS_DifferentDistributions as kaps


# ---------------------------------------------------------
# Build a dictionary mapping distribution names → generator
# ---------------------------------------------------------
def distributionList():
    """
    Creates and returns a dictionary of distribution generator
    functions for use in L-KAPS. Each entry corresponds to a
    specific parameterization of a distribution.
    """

    dists = {}

    # ----------------
    # Uniform distribution
    # ----------------
    dists[("uniform", 0)] = kaps.G_uniform()

    # ----------------
    # Normal distributions (σ = 1, 100, 10k, 1M)
    # ----------------
    for s in [10**i for i in range(-10, 10)]:
        name = ("normal", s)
        dists[name] = kaps.G_normal(mu=0, sigma=s)

    # ----------------------------------------------------------
    # Exponential distributions
    # λ values on a log scale: 10^-1 → 10^-9
    # ----------------------------------------------------------
    for l in range(-10, 10):
        lam = 10**l
        name = ("exponential", lam)
        dists[name] = kaps.G_exponential(lmbda=lam)

    # ----------------
    # Lognormal distributions
    # ----------------
    for s in [i/2 for i in range(1, 20)]:
        name = ("lognormal", s)
        dists[name] = kaps.G_lognormal(mu=0, sigma=s)

    # ----------------
    # Pareto distributions
    # ----------------
    for a in [i/10 for i in range(10, 100)]:
        name = ("pareto", a)
        dists[name] = kaps.G_pareto(xm=1.0, alpha=a)

    # ---------------------------------------------------------
    # Weibull distributions
    # k = shape, lam = scale (10^4 → 10^8)
    # ---------------------------------------------------------
    for k in [i/10 for i in range(1, 30)]:
        for l in range(2, 9):  # 10^4 up to 10^8
            lam = 10**l
            name = ("weibull", k, lam)
            dists[name] = kaps.G_weibull(k_shape=k, lam=lam)

    # ----------------
    # Logistic distributions
    # ----------------
    for s in [10**i for i in range(1, 10)]:
        name = ("logistic", s)
        dists[name] = kaps.G_logistic(mu=0, s=s)

    # ----------------
    # Zipf log
    # ----------------
    name = ("zipfLog", 0)
    dists[name] = kaps.G_zipf_log()

    # ----------------
    # Zipf–Pareto surrogate (for discrete data)
    # ----------------
    for a in [i/10 for i in range(11, 100)]:
        name = ("zipfpareto", a)
        dists[name] = kaps.G_zipf_pareto_surrogate(xmin=1, alpha=a)

    # ---------------------------------------------------------
    # Box–Cox family (under development)
    # ---------------------------------------------------------
    # for l in [-2, -1, -0.5, 0, 0.5, 1, 2]:
    #     name = f"boxcox_lambda{l}"
    #     dists[name] = kaps.G_boxcox(lmbd=l)

    return dists



# ---------------------------------------------------------
# L-KAPS core function
# Tests each distribution by computing total search depth
# across many quantiles × k-values
# ---------------------------------------------------------
def lkaps(arr):
    """
    Returns the best-fitting distribution for arr by computing
    the total search depth of K-Array Predictive Search across
    multiple quantiles and k-values.
    Lower total search depth = better match.
    """

    # Percentile checkpoints at which to probe array values
    positionCheckpoints = [
        0.1, 0.3, 0.5, 0.7, 0.9, 1.3, 1.8, 2.5, 3.5,
        5, 7, 10, 15, 20, 25, 30, 40, 50, 60, 70, 75,
        80, 85, 90, 92, 95, 97, 98, 99, 99.5, 99.8, 99.9
    ]

    # k-values for KAPS search depth evaluation
    k_values = [2, 4, 8, 16, 32, 64]

    # Load all distributions
    dists = distributionList()

    # Dictionary storing total search depth
    score = {}

    # ---------------------------------------------------------
    # Iterate over each distribution candidate
    # ---------------------------------------------------------
    for dist in dists:

        total_Depth = 0  # accumulated search depth across checkpoints

        # Iterate over percentile checkpoints
        for pos in positionCheckpoints:

            # Convert percentile → array index
            target = arr[int(pos * len(arr) / 100)]

            # Evaluate using all k-values
            for k in k_values:

                # Run KAPS and extract depth only
                output = kaps.kaps(
                    0,               # left index
                    len(arr) - 1,    # right index
                    arr,             # dataset
                    target,          # target element
                    k,               # k parameter
                    2,               # branching factor?
                    dists[dist]      # distribution generator
                )

                depth = output[1]   # output = (value, depth)
                total_Depth += depth

        # Store total depth for this distribution
        score[dist] = total_Depth

    # ---------------------------------------------------------
    # Determine distribution with minimum total search depth
    # ---------------------------------------------------------
    best_key, best_value = min(score.items(), key=lambda x: x[1])
    return best_key, best_value



# -----------------------------
# Example usage
# -----------------------------
# import GenerateData
#
# # Generate 1,000,000-sample array from exponential distribution
# arr = GenerateData.generate_array(10**6, dist="exponential", seed=1200)
#
# # Print best-fit distribution and total depth
# print(lkaps(arr))
