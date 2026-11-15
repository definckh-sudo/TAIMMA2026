"""CHẠY CHÍNH: một ván 15 vòng cho một chiến lược, ghi event log vào SQLite, in kết quả.
Ví dụ: python scripts/run_game.py --scenario pandemic --strategy S3 --budget 500 --seed 1"""
import argparse, _path  # noqa: F401
from agrisim.config import load_params, load_scenario
from agrisim.agents import STRATEGIES
from agrisim.engine.game import GameSession
from agrisim.storage.db import connect
from agrisim.storage.event_log import EventLogWriter, check_integrity
from agrisim.storage.export import export_table

ap = argparse.ArgumentParser()
ap.add_argument("--scenario", default="pandemic"); ap.add_argument("--strategy", default="S3")
ap.add_argument("--budget", type=float, default=500); ap.add_argument("--seed", type=int, default=20261106)
ap.add_argument("--rep", type=int, default=0); ap.add_argument("--decision-round", type=int, default=5)
ap.add_argument("--db", default="data/db/agrisim.db")
a = ap.parse_args()

con = connect(a.db); writer = EventLogWriter(con)
agent = STRATEGIES[a.strategy](budget=a.budget, decision_round=a.decision_round)
game = GameSession(load_scenario(a.scenario), load_params(), agent, seed=a.seed, replication=a.rep,
                   event_sink=writer)
writer.register_run(game, a.strategy)
res = game.run(); con.commit()
print("Log toàn vẹn:", check_integrity(con, game.run_id))
for k, v in res.items():
    print(f"{k:>16}: {v:.2f}" if isinstance(v, float) else f"{k:>16}: {v}")
for sh in game.player.shipments:
    s = sh.settlement
    print(f"  {sh.shipment_id}: đi vòng {sh.round_depart}, trễ {sh.port_delay}, đến vòng {s['arrival_round']}, "
          f"s_T={s['s_T']:.4f}, nhận={s['accepted']}, LC={s['LC']:.2f}, π={s['net_profit']:.2f}")
print("CSV:", export_table(con, "event"))
