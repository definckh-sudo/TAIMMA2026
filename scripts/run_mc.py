"""CHẠY CHÍNH: Monte Carlo E1 (H1, H2) và E2 (H3). Ví dụ: python scripts/run_mc.py --n 200"""
import argparse, _path  # noqa: F401
from pathlib import Path
from agrisim.sim.experiments import e1, e2
from agrisim.analysis.summary import summary_table
from agrisim.analysis.figures import boxplot_profit

ap = argparse.ArgumentParser(); ap.add_argument("--n", type=int, default=None, help="ghi đè N (mặc định theo config)")
a = ap.parse_args()
Path("data/results").mkdir(parents=True, exist_ok=True); Path("data/figures").mkdir(parents=True, exist_ok=True)
df = e1(a.n); df.to_csv("data/results/e1_results.csv", index=False)
tab = summary_table(df); tab.to_csv("data/results/e1_summary.csv", index=False)
print(tab[tab.B == 500][["scenario", "strategy", "mean", "p_loss", "cvar", "rank_mean"]].round(2).to_string(index=False))
boxplot_profit(df, "pandemic", 500, "data/figures/e1_box_pandemic_B500.pdf")
for row in e2():
    print("E2", row["pool"], row["f"], round(row["d_star"], 2), row["grid_argmax"])
