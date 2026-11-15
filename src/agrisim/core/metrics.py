"""EQ20: chỉ số Monte Carlo – mean, SD, MCSE, P(loss), CVaR, bootstrap ghép cặp."""
import numpy as np

def cvar(x, a=0.05):
    x = np.sort(np.asarray(x))
    return x[: max(1, int(np.ceil(a * len(x))))].mean()

def summary(x, a=0.05):
    x = np.asarray(x); n = len(x); sd = x.std(ddof=1); m = x.mean()
    return dict(mean=m, sd=sd, mcse=sd / np.sqrt(n), ci_lo=m - 1.96 * sd / np.sqrt(n),
                ci_hi=m + 1.96 * sd / np.sqrt(n), p_loss=(x < 0).mean(), cvar=cvar(x, a),
                p5=np.quantile(x, .05), p50=np.quantile(x, .5), p95=np.quantile(x, .95), n=n)

def paired_bootstrap(a, b, stat=np.mean, B=2000, seed=7):
    """KTC 95% của stat(a) − stat(b), lấy mẫu lại theo cặp replication (CRN)."""
    rng = np.random.default_rng(seed); a, b = np.asarray(a), np.asarray(b); n = len(a)
    v = np.empty(B)
    for j in range(B):
        i = rng.integers(0, n, n); v[j] = stat(a[i]) - stat(b[i])
    lo, hi = np.quantile(v, [0.025, 0.975])
    return dict(diff=stat(a) - stat(b), lo=lo, hi=hi)
