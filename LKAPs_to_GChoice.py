import KAPS_DifferentDistributions




def make_G_from_lkaps(arr, lkaps_result):
    """
    arr           : the sorted data array you're searching in
    lkaps_result  : tuple like ('uniform', 0) or ('pareto', 9.9) etc.
    returns       : a callable G(x) suitable to pass as G_choice into kaps()
    """
    name = lkaps_result[0].lower()
    params = lkaps_result[1:]

    # ---- Uniform ----
    if name == "uniform":
        # parameter often unused; we just use identity CDF proxy
        return KAPS_DifferentDistributions.G_uniform()

    # ---- Normal ----
    if name == "normal":
        if len(params) >= 2:
            mu, sigma = params[0], params[1]
        else:
            mu, sigma = KAPS_DifferentDistributions.fit_normal(arr)
        return KAPS_DifferentDistributions.G_normal(mu, sigma)

    # ---- Exponential ----
    if name == "exponential":
        if len(params) >= 1:
            lam = params[0]
        else:
            lam = KAPS_DifferentDistributions.fit_exponential(arr)
        return KAPS_DifferentDistributions.G_exponential(lam)

    # ---- Lognormal ----
    if name == "lognormal":
        if len(params) >= 2:
            mu, sigma = params[0], params[1]
        else:
            mu, sigma = KAPS_DifferentDistributions.fit_lognormal(arr)
        return KAPS_DifferentDistributions.G_lognormal(mu, sigma)

    # ---- Pareto ----
    if name == "pareto":
        # Your examples look like ('pareto', 9.9)
        # so we'll treat that as alpha and estimate xm from data
        if len(params) >= 2:
            xm, alpha = params[0], params[1]
        elif len(params) == 1:
            alpha = params[0]
            xm, _alpha_est = KAPS_DifferentDistributions.fit_pareto(arr)   # or xm = min(arr)
        else:
            xm, alpha = KAPS_DifferentDistributions.fit_pareto(arr)
        return KAPS_DifferentDistributions.G_pareto(xm, alpha)

    # ---- Weibull ----
    if name == "weibull":
        if len(params) >= 2:
            k_shape, lam = params[0], params[1]
        else:
            # if you don't have a Weibull fit yet, you can plug one in later
            # for now, just fall back to exponential-like behavior
            lam = KAPS_DifferentDistributions.fit_exponential(arr)
            k_shape = 1.0
        return KAPS_DifferentDistributions.G_weibull(k_shape, lam)

    # ---- Logistic ----
    if name == "logistic":
        if len(params) >= 2:
            mu, s = params[0], params[1]
        else:
            mu, s = KAPS_DifferentDistributions.fit_logistic(arr)
        return KAPS_DifferentDistributions.G_logistic(mu, s)

    # ---- Beta ----
    if name == "beta":
        if len(params) >= 2:
            alpha, beta_ = params[0], params[1]
        else:
            # you might want a separate Beta fit; placeholder here
            alpha, beta_ = 2.0, 2.0
        return KAPS_DifferentDistributions.G_beta(alpha, beta_)

    # ---- Zipf / discrete power law ----
    if name == "zipf":
        # simplest: log transform proxy
        return KAPS_DifferentDistributions.G_zipf_log()

    # ---- Box–Cox ----
    if name == "boxcox":
        if len(params) >= 1:
            lmbd = params[0]
        else:
            lmbd = 0.0
        return KAPS_DifferentDistributions.G_boxcox(lmbd)

    # Fallback: if we don't recognize the name, just use identity
    return KAPS_DifferentDistributions.G_uniform()
