from dataclasses import dataclass
from ..core import npc

@dataclass
class NPCTrader:
    """Tác tử arbitrage 'khứ hồi' (D12): số dư không giới hạn, trần lệnh mỗi vòng, không giữ tồn kho."""
    alpha: float
    threshold: float
    cap_share: float

    def act(self, pool, P_asia):
        direction, amount, X, Y = npc.npc_trade(pool.X, pool.Y, P_asia, pool.f,
                                                self.alpha, self.threshold, self.cap_share)
        gap_before = (P_asia - pool.price) / P_asia
        if direction != "no_op":
            pool.X, pool.Y = X, Y
            pool.state_version += 1
        return dict(direction=direction, amount=amount, gap_before=gap_before,
                    gap_after=(P_asia - pool.price) / P_asia)
