from dataclasses import dataclass, field
from enum import Enum

class ShipmentStatus(str, Enum):
    IN_TRANSIT = "in_transit"
    SETTLED = "settled"        # đã đến, được nhận, đã bán
    REJECTED = "rejected"      # đã đến nhưng s_T < s_min (D8)

@dataclass
class Shipment:
    """Lô hàng Asia → Europe (ĐT 5.1, BR07–BR09, BR12–BR14)."""
    shipment_id: str
    Q0: float
    Q_acquired: float
    gross_usdg: float          # ΔY_gross của giao dịch mua gốc
    round_depart: int
    T_base: int
    cold: bool
    phase_depart: int
    port_delay: int = 0
    elapsed_rounds: int = 0
    applied_event_ids: set = field(default_factory=set)   # chống áp event hai lần (PORT tests)
    status: ShipmentStatus = ShipmentStatus.IN_TRANSIT
    settlement: dict = field(default_factory=dict)

    @property
    def T_total(self):
        return self.T_base + self.port_delay

    @property
    def eta_round(self):
        return self.round_depart + self.T_total
