## NOTE: This is a test implementation of k-ary predictive search,
## still experimental and may need further adjustments.

# Tracks recursion depth for debugging / tracing
depth = 0

def kaps(lo, hi, arr, target, k, divisor, G_choice):

    global depth
    depth += 1

    # Fast rejects: target outside current window's value range
    if target < arr[lo] or target > arr[hi]:
        d = depth
        depth = 0
        return -1, d

    # Base case: interval collapsed to one element.
    if lo == hi:
        d = depth
        depth = 0
        return lo, depth if arr[lo] == target else -1, d

    # Avoid over-partitioning; keep k >= 1  (FIX #2)
    if hi - lo <= k:
        k = max(1, k // max(1, divisor))

    # Interpolation step in transformed space
    pos = interp_pos(arr, lo, hi, target, k, G_choice)

    # Compute integer bucket index and CLAMP to [0, k-1]  (FIX #1)
    import math
    b = int(math.floor(pos))
    if b < 0: b = 0
    elif b >= k: b = k - 1

    # Map bucket -> [subLo, subHi] (inclusive bounds)
    span = hi - lo
    subLo = lo + (span * b) // k
    subHi = lo + (span * (b + 1)) // k

    # Adjust sub-interval if target falls outside bucket boundaries.
    if target < arr[subLo]:
        subLo, subHi = lo, subLo
    elif target > arr[subHi]:
        subHi, subLo = hi, subHi
    else:
        # Direct hit checks for bucket edges.
        if arr[subLo] == target:
            d = depth
            depth = 0
            return subLo, d
        elif arr[subHi] == target:
            d = depth
            depth = 0
            return subHi, d
        # otherwise keep current [subLo, subHi]

    # Recurse if interval still >1 and k allows further partitioning.
    if subHi - subLo > 1 and k > 1:
        return kaps(subLo, subHi, arr, target, k, divisor, G_choice)  # (FIX #3)
    else:
        # Terminal step: at most two candidates left (loop over <=2 elements)
        for i in range(subLo, subHi + 1):
            if arr[i] == target:
                d = depth
                depth = 0
                return i, d
        d = depth
        depth = 0
        return -1, d






import math

# ---------- Core helper ----------
def interp_pos(arr, lo, hi, target, k, G):
    Ga, Gb, Gt = G(arr[lo]), G(arr[hi]), G(target)
    denom = Gb - Ga
    if denom == 0:
        return (k - 1) / 2.0
    return k * (Gt - Ga) / denom



# ---------- G(x) transforms by distribution ----------

# 1) Uniform(A,B): identity
def G_uniform():
    return lambda x: x

# 2) Normal(mu, sigma): Phi((x-mu)/sigma)
def G_normal(mu, sigma):
    if sigma <= 0: raise ValueError("sigma must be > 0")
    rt2 = math.sqrt(2.0)
    return lambda x: 0.5 * (1.0 + math.erf((x - mu) / (sigma * rt2)))

# 3) Exponential(lambda): 1 - exp(-lambda x), x >= 0
def G_exponential(lmbda):
    if lmbda <= 0: raise ValueError("lambda must be > 0")
    return lambda x: 1.0 - math.exp(-lmbda * max(x, 0.0))

# 4) Lognormal(mu, sigma): Phi((ln x - mu)/sigma), x > 0
def G_lognormal(mu, sigma):
    if sigma <= 0: raise ValueError("sigma must be > 0")
    rt2 = math.sqrt(2.0)
    return lambda x: 0.5 * (1.0 + math.erf((math.log(max(x, 1e-300)) - mu) / (sigma * rt2)))

# 5) Pareto(xm, alpha): 1 - (xm/x)^alpha, x >= xm > 0
def G_pareto(xm, alpha):
    if xm <= 0 or alpha <= 0: raise ValueError("xm, alpha must be > 0")
    def _G(x):
        if x < xm: return 0.0
        return 1.0 - (xm / x) ** alpha
    return _G

# 6) Weibull(k_shape, lam): 1 - exp(-(x/lam)^k), x >= 0
def G_weibull(k_shape, lam):
    if k_shape <= 0 or lam <= 0: raise ValueError("shape, scale must be > 0")
    return lambda x: 1.0 - math.exp(- (max(x, 0.0) / lam) ** k_shape)

# 7) Logistic(mu, s): 1/(1 + exp(-(x-mu)/s))
def G_logistic(mu, s):
    if s <= 0: raise ValueError("scale s must be > 0")
    return lambda x: 1.0 / (1.0 + math.exp(-(x - mu) / s))

# 8) Beta(alpha, beta) on [0,1]: exact needs betainc; else use a proxy
# Preferred (exact) if SciPy is available:
try:
    from math import isfinite  # stdlib
    from scipy.special import betainc  # regularized incomplete beta
    def G_beta(alpha, beta_):
        if alpha <= 0 or beta_ <= 0: raise ValueError("alpha,beta must be > 0")
        return lambda x: betainc(alpha, beta_, min(max(x, 0.0), 1.0))
except Exception:
    # Fallback: monotone logit proxy (works OK away from 0/1) or ECDF (recommended)
    def G_beta(alpha, beta_):
        # WARNING: proxy; consider using ECDF if you lack SciPy
        eps = 1e-9
        def logit(u): return math.log(u/(1.0-u))
        # map to roughly uniform via logit, then to [0,1] with a squashing
        return lambda x: 1.0 / (1.0 + math.exp(-logit(min(max(x, eps), 1.0-eps))))

# 9) Zipf / discrete power-law: practical proxies
# (a) simple log transform (robust, parameter-free)
def G_zipf_log():
    return lambda x: math.log(max(x, 1.0))

# (b) continuous Pareto surrogate with alpha and xmin
def G_zipf_pareto_surrogate(xmin, alpha):
    return G_pareto(xmin, alpha)

# 10) Box–Cox transform: (x^λ - 1)/λ  (λ→0 gives log)
def G_boxcox(lmbd):
    if abs(lmbd) < 1e-12:
        return lambda x: math.log(max(x, 1e-300))
    return lambda x: (max(x, 0.0) ** lmbd - 1.0) / lmbd











def fit_normal(arr):
    n = len(arr)
    mu = sum(arr)/n
    var = sum((x-mu)**2 for x in arr)/(n-1 if n>1 else 1)
    return mu, math.sqrt(max(var, 1e-300))

def fit_exponential(arr):                # assume x >= 0
    mean = sum(arr)/len(arr)
    return 1.0 / max(mean, 1e-300)

def fit_lognormal(arr):                  # assume x > 0
    logs = [math.log(max(x, 1e-300)) for x in arr]
    n = len(logs)
    mu = sum(logs)/n
    var = sum((z-mu)**2 for z in logs)/(n-1 if n>1 else 1)
    return mu, math.sqrt(max(var, 1e-300))

def fit_pareto(arr, xmin=None):          # Hill estimator
    xs = [x for x in arr if x > 0]
    if not xs: return 1.0, 1.0
    xm = xmin if xmin is not None else min(xs)
    ys = [math.log(x/xm) for x in xs if x >= xm]
    denom = sum(ys)
    alpha = len(ys) / max(denom, 1e-300)
    return xm, max(alpha, 1e-6)

def fit_logistic(arr):
    xs = sorted(arr)
    n = len(xs)
    median = xs[n//2] if n % 2 else 0.5*(xs[n//2-1]+xs[n//2])
    q1 = xs[n//4]
    q3 = xs[(3*n)//4]
    iqr = max(q3 - q1, 1e-300)
    s = iqr / (2.0*math.log(3.0))  # logistic IQR = 2 s ln 3
    return median, s
