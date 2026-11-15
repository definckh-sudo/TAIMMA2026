from dataclasses import dataclass, field

@dataclass
class MarketPath:
    """Đường giá thật của một thị trường đã sinh trước từ seed (D13). Index theo round (1-based)."""
    name: str
    base_price: float
    prices: dict = field(default_factory=dict)      # round -> giá thật
    epsilons: dict = field(default_factory=dict)    # round -> ε (lưu để tái dựng, ĐT 4.1)

    def price(self, r):
        return self.prices[r]
