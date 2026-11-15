"""Xuất CSV từ SQLite (không sửa dữ liệu gốc)."""
import csv
from pathlib import Path

def export_table(con, table, out_dir="data/results"):
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    cur = con.execute(f"SELECT * FROM {table}")
    path = Path(out_dir) / f"{table}.csv"
    with open(path, "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh); w.writerow([d[0] for d in cur.description]); w.writerows(cur)
    return path
