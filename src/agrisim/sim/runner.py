"""Chạy N replication cho mỗi chiến lược × kịch bản × ngân sách, dùng common random numbers:
cùng (seed, replication) -> cùng TruePath cho mọi chiến lược."""
import pandas as pd
from ..agents import STRATEGIES
from ..config import load_params, load_scenario
from ..engine.game import GameSession

def run_cell(scenario_id, strategy, budget, N, seed, decision_round=5, params=None):
    params = params or load_params()
    sc = load_scenario(scenario_id)
    rows = []
    for rep in range(N):
        agent = STRATEGIES[strategy](budget=budget, decision_round=decision_round)
        res = GameSession(sc, params, agent, seed=seed, replication=rep).run()
        rows.append(res | {"strategy": strategy, "B": budget})
    return pd.DataFrame(rows)

def run_experiment(cfg, N=None):
    frames = [run_cell(sc, st, B, N or cfg["N"], cfg["seed"], cfg["decision_round"])
              for sc in cfg["scenarios"] for st in cfg["strategies"] for B in cfg["budgets"]]
    return pd.concat(frames, ignore_index=True)
