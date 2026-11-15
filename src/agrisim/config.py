"""Nạp và kiểm tra cấu hình (ĐT mục 8.5): tham số, kịch bản, thí nghiệm. Không đặt tham số chìm trong code."""
import json
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = ROOT / "config"

@dataclass(frozen=True)
class Phase:
    phase: int; rounds: tuple; M_price: float; sigma: float; T_base: int; ship_mult: float
    lambda_mult: float; export_fee: float; pool_scale_on_enter: float; p_false_price: float
    name: str = ""; p_port: float = 0.0

@dataclass(frozen=True)
class Scenario:
    scenario_id: str; scenario_version: str; phases: tuple; port_events: dict

    def phase_of(self, r: int) -> Phase:
        """Vòng sau vòng cuối (settlement-only, D6) dùng tham số giai đoạn cuối."""
        for p in self.phases:
            if p.rounds[0] <= r <= p.rounds[1]:
                return p
        return self.phases[-1]

    def p_port(self, r: int) -> float:
        pe = self.port_events
        return pe.get("p_port", 0.0) if pe and pe["rounds"][0] <= r <= pe["rounds"][1] else 0.0

def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def load_params(version="v1.0"):
    p = load_json(CONFIG_DIR / f"parameters_{version}.json")
    assert p["amm"]["X0"] > 0 and p["amm"]["Y0"] > 0, "reserve phải dương"
    assert 0 <= p["amm"]["f"] < 1
    return p

def load_scenario(scenario_id):
    raw = load_json(CONFIG_DIR / "scenarios" / f"{scenario_id}.json")
    phases = tuple(Phase(**{k: (tuple(v) if k == "rounds" else v) for k, v in ph.items()})
                   for ph in raw["phases"])
    return Scenario(raw["scenario_id"], raw["scenario_version"], phases, raw.get("port_events") or {})

def load_experiment(name):
    return load_json(CONFIG_DIR / "experiments" / f"{name}.json")
