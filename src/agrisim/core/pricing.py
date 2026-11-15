"""EQ07: giá thị trường ngoài theo phase + nhiễu log-normal có hiệu chỉnh −σ²/2 (D14)."""
import numpy as np

def market_price(P0, M_phase, eps, sigma):
    """P = P0 · M · exp(ε − σ²/2), ε ~ N(0, σ²). Lưu riêng P0, M, ε khi log (ĐT 4.1)."""
    return P0 * M_phase * np.exp(eps - sigma ** 2 / 2)

def validate_price(p):
    """ĐT 6.5: giá không hữu hạn hoặc ≤ 0 -> run invalid (không clamp ngầm)."""
    p = np.asarray(p)
    return bool(np.all(np.isfinite(p)) and np.all(p > 0))
