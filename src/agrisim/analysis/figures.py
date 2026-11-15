"""Hình cho bài (xuất PDF vector – Feedback 3 mục 5.3): boxplot, histogram, π(Δ), bản đồ E3."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def boxplot_profit(df, scenario, B, path):
    sub = df[(df.scenario == scenario) & (df.B == B)]
    names = sorted(sub.strategy.unique())
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.boxplot([sub[sub.strategy == s]["profit"] for s in names], tick_labels=names)
    ax.axhline(0, ls="--", c="k", lw=1); ax.set_ylabel("π (USDG)"); ax.set_title(f"{scenario}, B = {B}")
    fig.tight_layout(); fig.savefig(path); plt.close(fig)
