"""Scenario Engine: sinh trước toàn bộ trạng thái thật của một replication (D13)."""
from dataclasses import dataclass
from ..core.pricing import market_price, validate_price
from ..domain.market import MarketPath
from .rng import stream

@dataclass
class TruePath:
    asia: MarketPath
    europe: MarketPath
    port_event: dict          # round -> bool
    last_round: int

def generate_true_path(scenario, params, seed0, replication):
    R = params["game"]["rounds"] + params["game"]["max_port_delay"]   # kể cả vòng settlement-only
    g_price = stream(seed0, scenario.scenario_id, replication, "market_price")
    g_port = stream(seed0, scenario.scenario_id, replication, "port_event")
    asia = MarketPath("asia", params["markets"]["asia"]["base_price"])
    europe = MarketPath("europe", params["markets"]["europe"]["base_price"])
    port = {}
    for r in range(1, R + 1):
        ph = scenario.phase_of(r)
        for mk in (asia, europe):
            eps = g_price.normal(0.0, ph.sigma)
            mk.epsilons[r] = eps
            mk.prices[r] = float(market_price(mk.base_price, ph.M_price, eps, ph.sigma))
        port[r] = bool(g_port.random() < scenario.p_port(r))
    if not validate_price(list(asia.prices.values()) + list(europe.prices.values())):
        raise ValueError("Run invalid: giá không hợp lệ (ĐT 6.5)")
    return TruePath(asia, europe, port, R)
