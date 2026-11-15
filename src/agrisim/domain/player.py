from dataclasses import dataclass, field
from ..core import ledger
from .shipment import Shipment

@dataclass
class Position:
    """Một lần mua gạo từ pool, dùng để phân bổ cost basis (ĐT 5.7)."""
    position_id: str
    gross_usdg: float
    rice_acquired: float
    rice_remaining: float
    round_bought: int

@dataclass
class Player:
    player_id: str
    cash: float
    positions: list = field(default_factory=list)
    shipments: list = field(default_factory=list)
    realized_profit: float = 0.0

    @property
    def rice(self):
        return sum(p.rice_remaining for p in self.positions)

    def add_position(self, gross_usdg, rice_out, r):
        self.positions.append(Position(f"POS{len(self.positions)+1}", gross_usdg, rice_out, rice_out, r))

    def _take(self, qty):
        """Lấy gạo theo FIFO, trả (lượng lấy, cost basis phân bổ theo tỷ lệ)."""
        qty = self.rice if qty <= 0 else min(qty, self.rice)
        left, basis = qty, 0.0
        for p in self.positions:
            if left <= 0: break
            q = min(left, p.rice_remaining)
            basis += p.gross_usdg * q / p.rice_acquired
            p.rice_remaining -= q; left -= q
        return qty, basis

    def sell_local(self, qty, P_asia):
        qty, basis = self._take(qty)
        revenue = P_asia * qty
        self.cash += revenue
        self.realized_profit += revenue - basis
        return dict(qty=qty, P_asia=P_asia, revenue=revenue, allocated_cost_basis=basis,
                    realized_net_profit=revenue - basis)

    def create_shipment(self, qty, r, phase, cold, shipment_id):
        qty, basis = self._take(qty)
        # Q_acquired = Q0 và gross = basis đã phân bổ => công thức (1) cho C_acq = basis
        sh = Shipment(shipment_id, Q0=qty, Q_acquired=qty, gross_usdg=basis, round_depart=r,
                      T_base=phase.T_base, cold=cold, phase_depart=phase.phase)
        self.shipments.append(sh)
        return sh
