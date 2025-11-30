
import numpy as np
import matplotlib.pyplot as plt
import random


import os, sys
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_PATH = os.path.join(PROJECT_ROOT, "src")
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

from kaps import lkaps
from kaps.l_kaps import distributionList
from kaps.generators import *



def _pk_from_arr(arr):
    """Return p_k = k/(N+1) for k = 1..N based on len(arr)."""
    N = len(arr)
    if N <= 0:
        return np.array([], dtype=float)
    return np.arange(1, N + 1, dtype=float) / (N + 1)


def _rescale_to_arr_range(arr, theo):
    """
    Linearly rescale theoretical values so they span [min(arr), max(arr)].
    This keeps the shape but matches the observed range.
    """
    arr = np.asarray(arr)
    theo = np.asarray(theo, dtype=float)

    if arr.size == 0 or theo.size == 0:
        return theo

    lo = float(np.min(arr))
    hi = float(np.max(arr))

    # if arr is constant, just return that constant
    if hi == lo:
        return np.full_like(theo, lo, dtype=float)

    tmin = float(theo[0])
    tmax = float(theo[-1])

    # if theoretical curve is flat, just map to lo
    if tmax == tmin:
        return np.full_like(theo, lo, dtype=float)

    scale = (hi - lo) / (tmax - tmin)
    return (theo - tmin) * scale + lo


# ---- helper: inverse CDF of standard normal (approx) ----

def _norm_ppf(p):
    """
    Approximate inverse CDF of standard normal using a
    rational approximation (Abramowitz-Stegun style).
    p must be in (0, 1).
    Works with numpy arrays.
    """
    p = np.asarray(p, dtype=float)

    # coefficients
    c0, c1, c2 = 2.515517, 0.802853, 0.010328
    d0, d1, d2 = 1.432788, 0.189269, 0.001308

    # split for symmetry
    mask = p < 0.5
    q = np.empty_like(p)

    # lower tail
    pl = p[mask]
    t = np.sqrt(-2.0 * np.log(pl))
    num = (c2 * t + c1) * t + c0
    den = ((d2 * t + d1) * t + d0) * t + 1.0
    q[mask] = -(t - num / den)

    # upper tail
    pu = p[~mask]
    t = np.sqrt(-2.0 * np.log(1.0 - pu))
    num = (c2 * t + c1) * t + c0
    den = ((d2 * t + d1) * t + d0) * t + 1.0
    q[~mask] = t - num / den

    return q


# ----------------- distributions ----------------- #

def give_exponential(arr, lmbd):
    """
    Expected order statistics for Exp(rate=lmbd),
    rescaled to [min(arr), max(arr)].
    """
    p = _pk_from_arr(arr)
    theo = -np.log(1.0 - p) / float(lmbd)
    return _rescale_to_arr_range(arr, theo)


def give_uniform(arr, a=0.0, b=1.0):
    """
    Expected order statistics for Uniform(a, b),
    rescaled to [min(arr), max(arr)].
    """
    p = _pk_from_arr(arr)
    theo = a + p * (b - a)
    return _rescale_to_arr_range(arr, theo)


def give_normal(arr, sigma, mu=0.0):
    """
    Expected order statistics for Normal(mu, sigma^2),
    rescaled to [min(arr), max(arr)].
    Uses an approximation for the inverse CDF.
    """
    p = _pk_from_arr(arr)
    z = _norm_ppf(p)
    theo = mu + float(sigma) * z
    return _rescale_to_arr_range(arr, theo)


def give_lognormal(arr, sigma, mu=0.0):
    """
    Expected order statistics for Lognormal with underlying
    Normal(mu, sigma^2), rescaled to [min(arr), max(arr)].
    """
    p = _pk_from_arr(arr)
    z = _norm_ppf(p)
    theo = np.exp(mu + float(sigma) * z)
    return _rescale_to_arr_range(arr, theo)


def give_pareto(arr, alpha, xm=1.0):
    """
    Expected order statistics for continuous Pareto(alpha, xm),
    CDF: F(x) = 1 - (xm/x)^alpha for x >= xm,
    rescaled to [min(arr), max(arr)].
    """
    p = _pk_from_arr(arr)
    theo = xm * (1.0 - p) ** (-1.0 / float(alpha))
    return _rescale_to_arr_range(arr, theo)


def give_weibull(arr, k_shape, lmbd):
    """
    Expected order statistics for Weibull(k_shape, lmbd),
    CDF: F(x) = 1 - exp(-(x/lmbd)^k),
    rescaled to [min(arr), max(arr)].
    """
    p = _pk_from_arr(arr)
    theo = float(lmbd) * (-np.log(1.0 - p)) ** (1.0 / float(k_shape))
    return _rescale_to_arr_range(arr, theo)


def give_logistic(arr, s, mu=0.0):
    """
    Expected order statistics for Logistic(mu, s),
    CDF: F(x) = 1 / (1 + exp(-(x-mu)/s)),
    rescaled to [min(arr), max(arr)].
    """
    p = _pk_from_arr(arr)
    theo = mu + float(s) * np.log(p / (1.0 - p))
    return _rescale_to_arr_range(arr, theo)


def give_zipf(arr, s, k_max=None):
    """
    Expected order statistics (quantiles) for discrete Zipf(s).
    Support is {1, 2, ..., k_max}. By default k_max = len(arr).
    Returns integer-valued quantiles, rescaled to [min(arr), max(arr)].
    """
    N = len(arr)
    if N <= 0:
        return np.array([], dtype=float)

    if k_max is None:
        k_max = N

    ks = np.arange(1, k_max + 1, dtype=float)
    weights = ks ** (-float(s))
    pmf = weights / weights.sum()
    cdf = np.cumsum(pmf)

    p = _pk_from_arr(arr)
    # search for smallest k with CDF >= p
    idx = np.searchsorted(cdf, p, side="left")
    theo = (idx + 1).astype(float)  # base Zipf support
    return _rescale_to_arr_range(arr, theo)


def give_zipf_pareto(arr, alpha, xm=1.0):
    """
    Zipf-Pareto style continuous power-law; here identical
    to a Pareto(alpha, xm) quantile, rescaled to [min(arr), max(arr)].
    """
    p = _pk_from_arr(arr)
    theo = xm * (1.0 - p) ** (-1.0 / float(alpha))
    return _rescale_to_arr_range(arr, theo)


# plt.plot(ind, arr)


dists_funcs = {
    "uniform": give_uniform,
    "normal": give_normal,
    "exponential": give_exponential,
    "lognormal": give_lognormal,
    "pareto": give_pareto,
    "weibull": give_weibull,
    "logistic": give_logistic,
    "zipf": give_zipf,
    "zipfpareto": give_zipf_pareto
}
dist_params = {
    "uniform": ["a", "b"],
    "normal": ["sigma", "mu"],
    "exponential": ["lmbd"],
    "lognormal": ["sigma", "mu"],
    "pareto": ["alpha", "xm"],
    "weibull": ["k_shape", "lmbd"],
    "logistic": ["s", "mu"],
    "zipf": ["s", "k_max"],
    "zipfpareto": ["alpha", "xm"]
}


def call_distribution(arr, dist_tuple):
    """
    dist_tuple = (name, param1, param2, ...)
    Example: ("weibull", 0.5, 10000)
    """
    name = dist_tuple[0]
    values = dist_tuple[1:]

    fn = dists_funcs[name]  # pick the function
    param_names = dist_params[name]  # list of parameter names

    # create keyword arguments dictionary
    kwargs = {param_names[i]: values[i] for i in range(len(values))}

    # call the function
    return fn(arr, **kwargs)


# ----------------------------------------------------------------------------------------------------------------------


# Generating random array from distribution
gen_functions = [
    gen_uniform,
    gen_zipf,
    gen_normal,
    gen_exponential,
    gen_lognormal,
    gen_pareto,
    gen_weibull,
    gen_logistic,
    gen_zipf_pareto
]
arr_length = 10**6
arr = sorted(random.choice(gen_functions)(arr_length))

# Using L-KAPs to get predict the distribution
best_name, best_score = lkaps(arr)
print("Best fit:", best_name)

# Creating a graph of the distribution predicted by L-KAPs
dists = distributionList()
gen = dists[best_name]
arr1 = call_distribution(arr, best_name)

# Plotting the two arrays to compare
plt.plot([i for i in range(len(arr))], arr, color='blue', label='Input Array')
plt.plot([i for i in range(len(arr))], arr1, color='green', label=f'Predicted Distribution: {best_name}')
plt.legend(loc='upper left')
plt.show()

