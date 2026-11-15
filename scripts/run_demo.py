"""DEMO nhanh: chạy S1–S4 trên cùng một diễn biến đại dịch (cùng seed) và so lợi nhuận."""
import _path  # noqa: F401
from agrisim.config import load_params, load_scenario
from agrisim.agents import STRATEGIES
from agrisim.engine.game import GameSession

params = load_params()
for sc in ("baseline", "pandemic"):
    for name, cls in STRATEGIES.items():
        res = GameSession(load_scenario(sc), params, cls(budget=500), seed=20261106, replication=0).run()
        print(f"{sc:<9} {name}: profit = {res['profit']:8.2f}  port_delay = {res['port_delay']}  rejected = {res['rejected']}")
