"""AMM constant-product: EQ01–EQ06, EQ16–EQ18 (đặc tả 04/11, mục 4.2–4.4, 8.2)."""
import numpy as np

def spot_price(X, Y):
    """EQ02: giá biên pool P_pool = Y / X (USDG/gạo)."""
    return Y / X

def quote_usdg_in(X, Y, dY_gross, f):
    """EQ03: đưa dY_gross USDG vào, trả về lượng gạo ra (chưa đổi state)."""
    dY_eff = (1 - f) * dY_gross
    return X * dY_eff / (Y + dY_eff)

def quote_rice_in(X, Y, dX_gross, f):
    """EQ03 chiều ngược (chỉ NPC dùng – D11): đưa gạo vào, nhận USDG."""
    dX_eff = (1 - f) * dX_gross
    return Y * dX_eff / (X + dX_eff)

def reserves_after_usdg_in(X, Y, dY_gross, f):
    """EQ04: pool nhận toàn bộ input gross (kể cả phí), mất phần gạo trả ra."""
    out = quote_usdg_in(X, Y, dY_gross, f)
    return X - out, Y + dY_gross

def reserves_after_rice_in(X, Y, dX_gross, f):
    out = quote_rice_in(X, Y, dX_gross, f)
    return X + dX_gross, Y - out

def execution_metrics(X, Y, dY_gross, f):
    """EQ05–EQ06 + mục 4.4: tách phí, price impact, output shortfall, sai lệch thực thi."""
    dY_eff = (1 - f) * dY_gross
    out = quote_usdg_in(X, Y, dY_gross, f)
    p_spot = Y / X
    p_curve = dY_eff / out
    p_exec = dY_gross / out
    ideal = X * dY_eff / Y
    return dict(fee_amount=f * dY_gross, P_spot_before=p_spot, P_curve_exec=p_curve,
                P_exec_actual=p_exec, price_impact_pct=p_curve / p_spot - 1,
                output_shortfall_pct=1 - out / ideal,
                total_execution_deviation_pct=p_exec / p_spot - 1)

def scale_pool(X, Y, s):
    """Pool-depth shock (D15): X, Y cùng nhân s; giá giữ nguyên, K_new = s² K_old."""
    return X * s, Y * s

def arbitrage_profit(X, Y, dY, P_market, f):
    """EQ16: mua gạo ở pool, bán ngay ở giá ngoài (không logistics)."""
    return P_market * quote_usdg_in(X, Y, dY, f) - dY

def optimal_trade_size(X, Y, P_market, f=0.0):
    """EQ17/EQ18: Δ* = (√((1−f)·K·P) − Y)/(1−f); f = 0 cho EQ17."""
    return (np.sqrt((1 - f) * X * Y * P_market) - Y) / (1 - f)
