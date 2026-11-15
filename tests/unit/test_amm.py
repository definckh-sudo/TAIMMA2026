"""UT-01, UT-02, UT-05 (H3) – giá trị kỳ vọng từ Feedback 3 mục 4.3."""
import pytest
from agrisim.core import amm
from agrisim.agents.arbitrage import argmax_vs_analytic

def test_ut01_invariant_no_fee():
    X, Y = amm.reserves_after_usdg_in(1000, 10000, 1000, 0.0)
    assert X * Y == pytest.approx(1000 * 10000)

def test_k_increases_with_fee():
    X, Y = amm.reserves_after_usdg_in(1000, 10000, 1000, 0.003)
    assert X * Y > 1e7

def test_a5_output():
    assert amm.quote_usdg_in(1000, 10000, 1000, 0) == pytest.approx(90.909, abs=1e-3)
    assert amm.quote_usdg_in(800, 8000, 1000, 0) == pytest.approx(88.89, abs=1e-2)

def test_ut02_impact_grows_with_size():
    small = amm.execution_metrics(1000, 10000, 100, 0.003)
    big = amm.execution_metrics(1000, 10000, 1000, 0.003)
    assert big["price_impact_pct"] > small["price_impact_pct"]
    assert big["total_execution_deviation_pct"] > big["price_impact_pct"]   # có thêm phí

@pytest.mark.parametrize("X,Y,f,d_exp,pmax", [(1000, 10000, 0, 1832.16, 335.68), (1000, 10000, 0.003, 1819.86, 330.19),
                                               (800, 8000, 0, 1465.73, 268.54), (800, 8000, 0.003, 1455.89, 264.16)])
def test_ut05_optimal_trade(X, Y, f, d_exp, pmax):
    r = argmax_vs_analytic(X, Y, 14.0, f)
    assert r["d_star"] == pytest.approx(d_exp, abs=0.01)
    assert abs(r["grid_argmax"] - r["d_star"]) <= 0.5
    assert r["max_profit"] == pytest.approx(pmax, abs=0.01)

def test_pool_shock_keeps_price():
    X, Y = amm.scale_pool(1000, 10000, 0.8)
    assert Y / X == pytest.approx(10) and X * Y == pytest.approx(0.64e7)
