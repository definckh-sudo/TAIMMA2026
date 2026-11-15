"""Chạy trọn ván 15 vòng: luồng vòng, D1 (thời điểm đến), D6 (chặn shipment muộn), log liên tục."""
from agrisim.config import load_params, load_scenario
from agrisim.agents import STRATEGIES
from agrisim.engine.game import GameSession

def _run(sc, st, **kw):
    g = GameSession(load_scenario(sc), load_params(), STRATEGIES[st](budget=500, **kw), seed=1, replication=0)
    return g, g.run()

def test_baseline_shipment_arrives_after_T_base():
    g, res = _run("baseline", "S2")
    sh = g.player.shipments[0]
    assert sh.settlement["arrival_round"] == 5 + 6 and sh.port_delay == 0

def test_pandemic_runs_and_settles():
    g, res = _run("pandemic", "S3")
    assert all(s.status.value != "in_transit" for s in g.player.shipments)
    assert [e.seq for e in g.events] == list(range(1, len(g.events) + 1))

def test_d6_blocks_late_shipment():
    g, res = _run("pandemic", "S2", decision_round=12)    # 12 + 8 > 15
    assert res["n_shipments"] == 0
    assert any(e.payload.get("reason_code") == "SHIPMENT_CANNOT_ARRIVE_BEFORE_END" for e in g.events)
