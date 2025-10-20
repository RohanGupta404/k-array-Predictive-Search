

import KAPS_DifferentDistributions as kaps
import GenerateData

# generating an exponential array
arr = GenerateData.generate_array(10**3, dist="exponential", seed=123687)


# Defining variables for the tests
positionCheckpoints = [0.1,0.3,0.5,0.7,0.9,1.3,1.8,2.5,3.5,5,7,10,15,20,25,30,40,50,60,70,75,80,85,90,92,95,97,98,99,99.5,99.8,99.9]
k_values = [2,4,8,16,32,64]


dists = {}

# Uniform
dists["uniform"] = kaps.G_uniform()

# Normal
for s in [1e0, 1e2, 1e4, 1e6]:
    name = f"normal(mu=0, sigma={s:g})"
    dists[name] = kaps.G_normal(mu=0, sigma=s)

# Exponential (λ on log scale: 10^-1 → 10^-15)
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
name = f"zipfLog()"
dists[name] = kaps.G_zipf_log()

# Zipf–Pareto surrogate (only if data discrete)
for a in [1.1, 1.5, 2.0, 3.0]:
    name = f"zipfpareto(xmin=1, alpha={a:g})"
    dists[name] = kaps.G_zipf_pareto_surrogate(xmin=1, alpha=a)

# # Box–Cox family
# for l in [-2, -1, -0.5, 0, 0.5, 1, 2]:
#     name = f"boxcox_lambda{l}"
#     dists[name] = kaps.G_boxcox(lmbd=l)





# Distribution scores
score = {}



if __name__ == "__main__":

    for dist in dists:

        total_Depth = 0

        for pos in positionCheckpoints:

            target = arr[int(pos * len(arr) / 100)]

            for k in k_values:

                output = kaps.kaps(0, len(arr) - 1, arr, target, k, 2, dists[dist])
                depth = output[1]

                total_Depth += depth

        score[dist] = total_Depth

for scr in score:
    print(f"{scr}: {score[scr]}")

best_key, best_value = min(score.items(), key=lambda x: x[1])
print(f"Best Distribution: {best_key}, with a search depth of {best_value}")

import matplotlib.pyplot as plt
plt.plot(arr)
plt.show()


