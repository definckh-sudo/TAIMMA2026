"""Tác tử H3: quét cỡ lệnh Δ trên lưới, so argmax với nghiệm đóng Δ* (E2, UT-05)."""
import numpy as np
from ..core import amm

def profit_curve(X, Y, P_market, f, grid):
    grid = np.asarray(grid, dtype=float)
    return grid, amm.arbitrage_profit(X, Y, grid, P_market, f)

def argmax_vs_analytic(X, Y, P_market, f, step=0.5, stop=4000):
    g, prof = profit_curve(X, Y, P_market, f, np.arange(0, stop, step))
    d_star = amm.optimal_trade_size(X, Y, P_market, f)
    return dict(grid_argmax=g[prof.argmax()], d_star=d_star, max_profit=prof.max(),
                rel_error=abs(g[prof.argmax()] - d_star) / d_star)
