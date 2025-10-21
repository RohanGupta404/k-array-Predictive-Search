import KAPS_DifferentDistributions as kaps
import GenerateData
#import matplotlib.pyplot as plt
import time
import math

# ---------------------------------------------
# Generate a sample array for testing
# ---------------------------------------------
# Here we're generating an exponential dataset with 10^3 elements.
# The "seed" ensures repeatability of random values.
arr = GenerateData.generate_array(10**5, dist="exponential", seed=1234)

# ---------------------------------------------
# Define test configuration
# ---------------------------------------------
# Checkpoints (percentile positions within the array)
# and the different k-values to test KAPS performance.
positionCheckpoints = [0.1,0.3,0.5,0.7,0.9,1.3,1.8,2.5,3.5,5,7,10,15,20,25,30,40,50,60,70,75,80,85,90,92,95,97,98,99,99.5,99.8,99.9]
k_values = [2,4,8,16,32,64]

# ---------------------------------------------
# Define candidate distributions
# ---------------------------------------------
dists = {}

# Uniform
dists["uniform"] = kaps.G_uniform()

# Normal
for s in [1e0, 1e2, 1e4, 1e6]:
    name = f"normal(mu=0, sigma={s:g})"
    dists[name] = kaps.G_normal(mu=0, sigma=s)

# Exponential (λ on log scale: 10^-1 → 10^-9)
for l in range(-1, -10, -1):
    lam = 10**l
    name = f"exponential(lambda={lam:.0e})"
    dists[name] = kaps.G_exponential(lmbda=lam)

# Lognormal
for s in [0.5, 1.0, 2.0, 3.0]:
    name = f"lognormal(mu=0, sigma={s:g})"
    dists[name] = kaps.G_lognormal(mu=0, sigma=s)

# Pareto
for a in [1.1, 1.5, 2.0, 3.0, 5.0]:
    name = f"pareto(xm=1.0, alpha={a:g})"
    dists[name] = kaps.G_pareto(xm=1.0, alpha=a)

# Weibull (k-shape × λ-scale grid)
for k in [0.3, 0.5, 1.0, 1.5, 2.0]:
    for l in range(4, 9):  # 10^4 ... 10^8
        lam = 10**l
        name = f"weibull(k_shape={k:g}, lam={lam:.0e})"
        dists[name] = kaps.G_weibull(k_shape=k, lam=lam)

# Logistic
for s in [10, 100, 1000, 10000]:
    name = f"logistic(mu=0, s={s:g})"
    dists[name] = kaps.G_logistic(mu=0, s=s)

# Zipf log
name = "zipfLog()"
dists[name] = kaps.G_zipf_log()

# Zipf–Pareto surrogate (only if data discrete)
for a in [1.1, 1.5, 2.0, 3.0]:
    name = f"zipfpareto(xmin=1, alpha={a:g})"
    dists[name] = kaps.G_zipf_pareto_surrogate(xmin=1, alpha=a)

# Initialize dictionary to store distribution scores
score = {}

# ==========================================================
# Main executable block — only runs if file is executed directly
# ==========================================================
if __name__ == "__main__":

    start = time.perf_counter()

    # Loop over each candidate distribution
    for dist in dists:

        total_Depth = 0  # track cumulative depth for this distribution

        # For each checkpoint position in the array
        for pos in positionCheckpoints:
            target = arr[int(pos * len(arr) / 100)]  # target element by percentile

            # Test with different k values
            for k in k_values:
                # Run the KAPS search and extract the depth
                output = kaps.kaps(0, len(arr) - 1, arr, target, k, 2, dists[dist])
                depth = output[1]
                wasted_depth = depth - math.log(len(arr), k)
                total_Depth += wasted_depth

        # Store total depth score for this distribution
        score[dist] = total_Depth

    # ---------------------------------------------
    # Display results
    # ---------------------------------------------
    for scr in score:
        print(f"{scr}: {score[scr]}")

    # Find the distribution with the smallest total depth
    best_key, best_value = min(score.items(), key=lambda x: x[1])
    print(f"\nBest Distribution: {best_key}, with total wasted depth of {best_value}")

    # ---------------------------------------------
    # Plot the generated data for visualization
    # ---------------------------------------------
    #plt.plot(arr)
    #plt.title("Generated Data Array (Sorted)")
    #plt.xlabel("Index")
    #plt.ylabel("Value")
    #plt.show()

    end = time.perf_counter()

    elapsed = end - start
    print(f"Execution time: {elapsed:.9f} seconds")
