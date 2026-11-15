"""RT-01 / T17: cùng seed -> cùng kết quả; các chiến lược gặp cùng đường giá (CRN)."""
from agrisim.config import load_params, load_scenario
from agrisim.agents import STRATEGIES
from agrisim.engine.game import GameSession

def test_same_seed_same_result():
    a = GameSession(load_scenario("pandemic"), load_params(), STRATEGIES["S2"](), seed=9).run()
    b = GameSession(load_scenario("pandemic"), load_params(), STRATEGIES["S2"](), seed=9).run()
    assert a["profit"] == b["profit"]

def test_common_random_numbers():
    g1 = GameSession(load_scenario("pandemic"), load_params(), STRATEGIES["S1"](), seed=9)
    g2 = GameSession(load_scenario("pandemic"), load_params(), STRATEGIES["S3"](), seed=9)
    assert g1.true_path.europe.prices == g2.true_path.europe.prices
    assert g1.true_path.port_event == g2.true_path.port_event
