"""IT-01, IT-02, IT-04 – bộ số kiểm thử của thầy (Feedback 3 mục 4.1, r_c = 0, ±0,01)."""
import pytest
from agrisim.core import amm, logistics, ledger

Q = amm.quote_usdg_in(1000, 10000, 1000, 0.0)

@pytest.mark.parametrize("PE,lam,T,cs,e,cold,exp", [
    (13, .010, 6, .50, 0, 0, -16.43), (13, .010, 6, .50, 0, 1, -18.65),
    (18, .015, 10, 1.25, .15, 0, 54.10), (18, .015, 11, 1.25, .15, 0, -1263.64),
    (18, .015, 10, 1.25, .15, 1, 128.61), (18, .015, 11, 1.25, .15, 1, 117.22),
    (18, .015, 13, 1.25, .15, 1, 94.71)])
def test_teacher_values(PE, lam, T, cs, e, cold, exp):
    s = logistics.survival(logistics.lambda_effective(lam, 1.0, cold, 0.5), T)
    r = ledger.export_settlement(1000, Q, Q, s, PE, e=e, c_ship=cs, C_cold=0.4, cold=cold,
                                 tau=0.08, s_min=0.85, r_c=0.0, T=T)
    assert r["net_profit"] == pytest.approx(exp, abs=0.01)

def test_capital_cost_example():
    s = logistics.survival(0.015, 10)
    r = ledger.export_settlement(1000, Q, Q, s, 18, e=.15, c_ship=1.25, C_cold=.4, cold=0,
                                 tau=.08, s_min=.85, r_c=.002, T=10)
    assert r["capital_cost"] == pytest.approx(25.27, abs=.01) and r["net_profit"] == pytest.approx(28.83, abs=.01)

def test_local_sale_pro_rata():
    r = ledger.local_sale(14, Q / 2, 1000, Q)
    assert r["allocated_cost_basis"] == pytest.approx(500)

def test_boundaries():
    assert logistics.survival(0.0, 10) == 1.0
    assert logistics.survival(0.01, 8) < logistics.survival(0.01, 6)
