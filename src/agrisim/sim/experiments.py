"""Định nghĩa E1–E3 (Feedback 3 mục 5.2). E3 cần ghi đè tham số -> tạo parameter version mới."""
import copy
from ..config import load_experiment, load_params
from .runner import run_experiment

def e1(N=None):
    return run_experiment(load_experiment("e1_strategies"), N)

def e2():
    from ..agents.arbitrage import argmax_vs_analytic
    cfg = load_experiment("e2_trade_size")
    return [dict(pool=p, f=f, **argmax_vs_analytic(p[0], p[1], cfg["P_m_asia"], f))
            for p in cfg["pools"] for f in cfg["fees"]]

def e3_one_way(param_path, values, N=200):
    """TODO: quét một chiều; ghi version tham số vào kết quả."""
    base = load_params()
    out = []
    for v in values:
        p = copy.deepcopy(base); sect, key = param_path
        p[sect][key] = v
        out.append((v, p))
    return out
