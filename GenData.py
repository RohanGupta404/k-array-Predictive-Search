import numpy as np
import matplotlib.pyplot as plt


def gen_uniform(N, low=0, high=None, rng=None):
    if high is None:
        high = N * 100
    # keep style: ignore rng, use np.random directly like original
    x = np.random.uniform(low, high, N)
    return np.sort(x)


def gen_zipf(N, a=2.0, cap=10**12, rng=None):
    x = (rng or np.random).zipf(a, N)
    x = np.minimum(x, cap)
    return np.sort(x)


def gen_normal(N, mu=0, sigma=0.1):
    x = np.random.normal(mu, sigma, N)
    return np.sort(x)


def gen_exponential(N, lmbd=1):
    # note: scale = lmbd (mean), matching your original
    x = np.random.default_rng().exponential(scale=lmbd, size=N)
    return np.sort(x)


# -------- NEW GENERATORS (same style) -------- #

def gen_lognormal(N, mu=0.0, sigma=0.1):
    """
    Lognormal with underlying Normal(mu, sigma^2).
    """
    x = np.random.lognormal(mean=mu, sigma=sigma, size=N)
    return np.sort(x)


def gen_pareto(N, alpha=1.0, xm=1.0):
    """
    Continuous Pareto(alpha, xm),
    using: X = xm * (1 + Y), Y ~ Pareto(alpha) in NumPy's parameterization.
    """
    y = np.random.pareto(alpha, N)
    x = xm * (1.0 + y)
    return np.sort(x)


def gen_weibull(N, k_shape=1.5, lmbd=1.0):
    """
    Weibull(k_shape, lmbd),
    NumPy Weibull gives shape-only: scale by lmbd.
    """
    y = np.random.weibull(k_shape, N)
    x = lmbd * y
    return np.sort(x)


def gen_logistic(N, mu=0.0, s=1.0):
    """
    Logistic(mu, s),
    generated via inverse CDF:
    X = mu + s * log(U / (1 - U)), U ~ Uniform(0,1).
    """
    u = np.random.random(N)
    x = mu + s * np.log(u / (1.0 - u))
    return np.sort(x)


def gen_zipf_pareto(N, alpha=1.0, xm=1.0):
    """
    "Zipf-Pareto" style generator.
    Here we mimic a continuous power-law like Pareto(alpha, xm).
    If you later want a different hybrid, you can just swap this body.
    """
    y = np.random.pareto(alpha, N)
    x = xm * (1.0 + y)
    return np.sort(x)


# --- quick example (commented out) ---
# arr = gen_exponential(10**2, 100)
# plt.plot(arr)
# plt.show()
