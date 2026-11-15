"""EQ08–EQ09 + D12: NPC arbitrage kéo giá pool một phần α về giá ngoài châu Á."""
import numpy as np

def target_price(P_pool, P_asia, alpha):
    """EQ08: P_target = (1 − α)·P_pool + α·P_asia."""
    return (1 - alpha) * P_pool + alpha * P_asia

def npc_trade(X, Y, P_asia, f, alpha, threshold, cap_share):
    """Tìm cỡ lệnh có phí đưa giá pool tới P_target (nghiệm đóng tương đương bisection).
    Trả (direction, amount, X_new, Y_new); direction ∈ {'buy_rice','sell_rice','no_op'}."""
    P = Y / X
    if abs(P_asia - P) / P_asia <= threshold:
        return "no_op", 0.0, X, Y
    Pt = target_price(P, P_asia, alpha)
    a = 1 - f
    if P < P_asia:          # pool rẻ: NPC đưa USDG vào mua gạo
        b, c = (2 - f) * Y, Y ** 2 - Pt * X * Y
        d = min((-b + np.sqrt(b * b - 4 * a * c)) / (2 * a), cap_share * Y)
        return "buy_rice", d, X * Y / (Y + a * d), Y + d
    b, c = (2 - f) * X, X ** 2 - X * Y / Pt   # pool đắt: NPC đưa gạo vào
    d = min((-b + np.sqrt(b * b - 4 * a * c)) / (2 * a), cap_share * Y / P)
    return "sell_rice", d, X + d, X * Y / (X + a * d)
