import pandas as pd
from ..core.metrics import summary

def summary_table(df, by=("scenario", "B", "strategy")):
    rows = [dict(zip(by, k)) | summary(g["profit"].values) for k, g in df.groupby(list(by))]
    out = pd.DataFrame(rows)
    out["rank_mean"] = out.groupby(list(by[:-1]))["mean"].rank(ascending=False).astype(int)
    out["rank_cvar"] = out.groupby(list(by[:-1]))["cvar"].rank(ascending=False).astype(int)
    return out
