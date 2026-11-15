"""Sổ chi phí D7 (Feedback 3 mục 2.2) – công thức (1)–(5) + bán nội địa (ĐT 5.7)."""

def cost_acquired(dY_gross, Q0, Q_acquired):                       # (1)
    return dY_gross * Q0 / Q_acquired

def cash_out(C_acq, e, c_ship, Q0, C_cold, cold):                  # (2)
    return C_acq * (1 + e) + c_ship * Q0 + C_cold * Q0 * (1 if cold else 0)

def landed_cost(C_out, tau, C_acq, c_ship, Q0, is_accepted, r_c, T):   # (3)
    duty = tau * (C_acq + c_ship * Q0) * (1 if is_accepted else 0)
    capital = r_c * C_out * T
    return C_out + duty + capital, duty, capital

def quantity_sold(Q0, s_T, s_min):                                   # (4)
    return Q0 * s_T if s_T >= s_min else 0.0

def net_profit(P_E_arr, Q_sell, LC):                                 # (5)
    return P_E_arr * Q_sell - LC

def export_settlement(dY_gross, Q_acquired, Q0, s_T, P_E_arr, *, e, c_ship, C_cold,
                      cold, tau, s_min, r_c, T):
    """Ghép (1)–(5) cho một shipment; trả dict để log/debrief (waterfall LC)."""
    C_acq = cost_acquired(dY_gross, Q0, Q_acquired)
    C_out = cash_out(C_acq, e, c_ship, Q0, C_cold, cold)
    acc = s_T >= s_min
    LC, duty, capital = landed_cost(C_out, tau, C_acq, c_ship, Q0, acc, r_c, T)
    Q_sell = quantity_sold(Q0, s_T, s_min)
    return dict(C_acq=C_acq, export_fee=C_acq * e, shipping=c_ship * Q0,
                cold_cost=C_cold * Q0 * (1 if cold else 0), C_out=C_out, import_duty=duty,
                capital_cost=capital, LC=LC, accepted=acc, Q_sell=Q_sell,
                revenue=P_E_arr * Q_sell, net_profit=net_profit(P_E_arr, Q_sell, LC))

def local_sale(P_asia, qty_sold, gross_usdg_input, rice_acquired):
    """ĐT 5.7: phân bổ giá vốn theo tỷ lệ, không trừ phí hai lần."""
    allocated = gross_usdg_input * qty_sold / rice_acquired
    revenue = P_asia * qty_sold
    return dict(revenue=revenue, allocated_cost_basis=allocated, realized_net_profit=revenue - allocated)
