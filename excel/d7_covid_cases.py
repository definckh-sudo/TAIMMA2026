"""
AgriSim Global – Tính lợi nhuận lô hàng xuất khẩu Asia -> Europe theo sổ chi phí D7
(Feedback từ thầy – file 3, mục 2.2, quyết định D7, công thức (1)-(5)) cho các tình huống COVID-19.

Chạy:  python d7_covid_cases.py
Đầu ra: in bảng từng bước ra màn hình + d7_results.csv (đối chiếu với file Excel).
"""
import csv

# ---------------------------------------------------------------------------
# 1. THAM SỐ CHUNG (Bảng tham số khóa v1.0 – Feedback 3, mục 3; giả định chung mục 4.1)
# ---------------------------------------------------------------------------
X_POOL, Y_POOL = 1000.0, 10000.0   # pool châu Á: 1.000 gạo / 10.000 USDG (giá pool 10)
F_SWAP = 0.0                       # phí swap f = 0 như bộ số kiểm thử mục 4.1
B = 1000.0                         # ngân sách mua = ΔY_gross (USDG)
LAMBDA0 = 0.01                     # λ nền 1%/vòng (PAR06)
RHO_COLD, C_COLD = 0.5, 0.4        # PAR07: bảo quản giảm λ 50%, tốn 0,4 USDG/đơn vị
TAU = 0.08                         # thuế nhập khẩu 8% trên CIF (PAR10)
S_MIN = 0.85                       # ngưỡng nhận hàng (PAR09)
R_C = 0.002                        # chi phí vốn 0,2%/vòng (PAR11); đặt 0 để khớp bảng mục 4.1

# ---------------------------------------------------------------------------
# 2. CÁC TÌNH HUỐNG (bám Phụ lục A4/A7 proposal và D5, D3, mục 4.1 Feedback 3)
#    q0_share = tỷ lệ lượng gạo đưa lên tàu so với lượng mua được (1 = xuất cả lô)
# ---------------------------------------------------------------------------
CASES = [
    # mã, tên, P_A, P_E,arr, hệ số λ, T_base, port delay, c_ship, e, q0_share
    ("TH0", "Trước dịch (baseline)",                    10.00, 13.00, 1.0,  6, 0, 0.50, 0.00, 1.0),
    ("TH1", "COVID – cú sốc, hàng đến đúng hạn",         14.00, 18.00, 1.5, 10, 0, 1.25, 0.15, 1.0),
    ("TH2", "COVID – cú sốc + 1 vòng tắc cảng",          14.00, 18.00, 1.5, 10, 1, 1.25, 0.15, 1.0),
    ("TH3", "COVID – cú sốc + 3 vòng tắc cảng",          14.00, 18.00, 1.5, 10, 3, 1.25, 0.15, 1.0),
    ("TH4", "COVID – phục hồi (GĐ3)",                    11.50, 14.95, 1.2,  8, 0, 0.80, 0.05, 1.0),
    ("TH5", "COVID – cú sốc, xuất 1/2 lô, 1/2 bán nội địa", 14.00, 18.00, 1.5, 10, 0, 1.25, 0.15, 0.5),
]

# ---------------------------------------------------------------------------
# 3. CÁC HÀM TÍNH
# ---------------------------------------------------------------------------
def amm_buy(dY_gross, X=X_POOL, Y=Y_POOL, f=F_SWAP):
    """EQ03: lượng gạo nhận về khi đưa ΔY_gross USDG vào pool."""
    dY_eff = (1 - f) * dY_gross
    return X * dY_eff / (Y + dY_eff)

def d7(case, cold, r_c=R_C):
    code, name, PA, PE, lam_mult, T_base, delay, c_ship, e, share = case
    Q_acq = amm_buy(B)                                    # lượng gạo mua được
    Q0 = share * Q_acq                                    # lượng đưa lên tàu
    T = T_base + delay                                    # T_elapsed (D1, D3)
    lam_eff = LAMBDA0 * lam_mult * (1 - RHO_COLD * cold)  # EQ11
    s_T = (1 - lam_eff) ** T                              # EQ10
    acc = 1 if s_T >= S_MIN else 0                        # EQ12

    C_acq = B * Q0 / Q_acq                                # (1)
    C_out = C_acq * (1 + e) + c_ship * Q0 + C_COLD * Q0 * cold          # (2)
    duty = TAU * (C_acq + c_ship * Q0) * acc              # thành phần thuế trong (3)
    cap = r_c * C_out * T                                 # thành phần chi phí vốn trong (3)
    LC = C_out + duty + cap                               # (3)
    Q_sell = Q0 * s_T if acc else 0.0                     # (4)
    revenue = PE * Q_sell
    pi = revenue - LC                                     # (5)

    # phần không xuất (TH5) bán ngay tại châu Á, phân bổ giá vốn theo tỷ lệ (ĐT mục 5.7)
    Q_local = Q_acq - Q0
    pi_local = PA * Q_local - B * Q_local / Q_acq
    return dict(code=code, name=name, cold=cold, P_A=PA, P_E=PE, Q_acq=Q_acq, Q0=Q0, T=T,
                lam_eff=lam_eff, s_T=s_T, accepted=acc, C_acq=C_acq,
                export_fee=C_acq * e, ship=c_ship * Q0, cold_cost=C_COLD * Q0 * cold,
                C_out=C_out, duty=duty, capital=cap, LC=LC, Q_sell=Q_sell,
                spoil_qty=Q0 - Q_sell, revenue=revenue, pi=pi,
                margin=pi / C_acq, pi_local_part=pi_local, pi_total=pi + pi_local,
                pi_rc0=None)

def s1_local(case):
    """Chiến lược tham chiếu S1: bán toàn bộ tại châu Á (không dùng D7)."""
    Q = amm_buy(B)
    return case[2] * Q - B

# ---------------------------------------------------------------------------
# 4. CHẠY, KIỂM TRA VÀ XUẤT KẾT QUẢ
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Kiểm tra với bộ số của thầy (Feedback 3 mục 4.1, r_c = 0, sai số ±0,01)
    expected = {("TH0", 0): -16.43, ("TH0", 1): -18.65, ("TH1", 0): 54.10, ("TH2", 0): -1263.64,
                ("TH1", 1): 128.61, ("TH2", 1): 117.22, ("TH3", 1): 94.71}
    for (code, cold), exp in expected.items():
        case = next(c for c in CASES if c[0] == code)
        got = d7(case, cold, r_c=0.0)["pi"]
        assert abs(got - exp) < 0.01, (code, cold, got, exp)
    assert abs(d7(CASES[1], 0)["pi"] - 28.83) < 0.01        # ví dụ có r_c = 0,2%: π = 28,83
    print("Khớp toàn bộ giá trị kiểm thử của thầy (±0,01).\n")

    rows = []
    for case in CASES:
        for cold in (0, 1):
            r = d7(case, cold)
            r["pi_rc0"] = d7(case, cold, r_c=0.0)["pi"]
            r["pi_S1_local"] = s1_local(case)
            rows.append(r)

    keys = ["code", "cold", "T", "s_T", "accepted", "C_acq", "C_out", "duty", "capital",
            "LC", "Q_sell", "revenue", "pi", "pi_rc0", "pi_total", "pi_S1_local"]
    print(" | ".join(f"{k:>9}" for k in keys))
    for r in rows:
        print(" | ".join(f"{r[k]:>9.4f}" if isinstance(r[k], float) else f"{r[k]:>9}" for k in keys))

    with open("d7_results.csv", "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    print("\nĐã ghi d7_results.csv")
