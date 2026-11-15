from dataclasses import dataclass
from ..core import amm

@dataclass
class Pool:
    """AMM pool rice–USDG tại châu Á (một pool duy nhất trong MVP)."""
    X: float
    Y: float
    f: float
    state_version: int = 0

    @property
    def price(self):
        return amm.spot_price(self.X, self.Y)

    def quote_buy_rice(self, usdg_in):
        """Quote không đổi state (ĐT 4.3)."""
        return amm.quote_usdg_in(self.X, self.Y, usdg_in, self.f)

    def buy_rice(self, usdg_in):
        out = self.quote_buy_rice(usdg_in)
        self.X, self.Y = amm.reserves_after_usdg_in(self.X, self.Y, usdg_in, self.f)
        self.state_version += 1
        return out

    def scale(self, s):
        """Pool-depth shock, áp đúng một lần khi đổi phase (D15)."""
        self.X, self.Y = amm.scale_pool(self.X, self.Y, s)
        self.state_version += 1

    def snapshot(self):
        return dict(X=self.X, Y=self.Y, P_pool=self.price, K=self.X * self.Y, state_version=self.state_version)
