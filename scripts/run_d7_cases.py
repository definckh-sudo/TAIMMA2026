"""Tính các tình huống COVID-19 theo sổ chi phí D7 bằng core/ledger (đối chiếu file Excel)."""
import _path  # noqa: F401
from agrisim.core import amm, logistics, ledger

Q = amm.quote_usdg_in(1000, 10000, 1000, 0.0)
CASES = [("TH0 trước dịch", 13, 1.0, 6, 0.50, 0.00), ("TH1 cú sốc", 18, 1.5, 10, 1.25, 0.15),
         ("TH2 cú sốc +1 trễ", 18, 1.5, 11, 1.25, 0.15), ("TH3 cú sốc +3 trễ", 18, 1.5, 13, 1.25, 0.15),
         ("TH4 phục hồi", 14.95, 1.2, 8, 0.80, 0.05)]
for name, PE, lm, T, cs, e in CASES:
    for cold in (0, 1):
        s = logistics.survival(logistics.lambda_effective(0.01, lm, cold, 0.5), T)
        r = ledger.export_settlement(1000, Q, Q, s, PE, e=e, c_ship=cs, C_cold=0.4, cold=cold,
                                     tau=0.08, s_min=0.85, r_c=0.002, T=T)
        print(f"{name:<20} cold={cold} s_T={s:.4f} LC={r['LC']:9.2f} π={r['net_profit']:9.2f}")
