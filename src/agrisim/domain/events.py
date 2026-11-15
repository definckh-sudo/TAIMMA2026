"""Kiểu sự kiện chuẩn cho event log (ĐT 9.1, GAME04). Mỗi event có state_before/after."""
from dataclasses import dataclass, field, asdict
from enum import Enum

class EventType(str, Enum):
    PHASE_CHANGE = "phase_change"
    POOL_DEPTH_SHOCK = "pool_depth_shock"
    MARKET_PRICE_UPDATE = "market_price_update"
    PORT_EVENT = "port_event"
    HINT_DISPLAYED = "hint_displayed"
    SWAP_CONFIRM = "swap_confirm"
    LOCAL_SALE = "local_sale"
    SHIPMENT_CREATE = "shipment_create"
    SHIPMENT_UPDATE = "shipment_update"
    SHIPMENT_SETTLEMENT = "shipment_settlement"
    NPC_ARBITRAGE = "npc_arbitrage"
    ACTION_REJECTED = "action_rejected"
    ROUND_SNAPSHOT = "round_snapshot"

@dataclass
class Event:
    run_id: str
    round: int
    seq: int
    event_type: EventType
    actor: str
    payload: dict = field(default_factory=dict)
    state_before: dict = field(default_factory=dict)
    state_after: dict = field(default_factory=dict)

    def to_row(self):
        d = asdict(self); d["event_type"] = self.event_type.value
        return d
