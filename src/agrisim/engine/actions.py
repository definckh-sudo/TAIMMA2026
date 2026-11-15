"""Hành động người chơi/tác tử và kiểm tra hợp lệ (BR05, D6, D11)."""
from dataclasses import dataclass

@dataclass
class Action:
    kind: str                 # 'buy' | 'sell_local' | 'ship' | 'cancel'
    amount: float = 0.0       # buy: USDG; sell_local/ship: lượng gạo (<=0 nghĩa là toàn bộ)
    cold: bool = False

def validate(action, player, r, T_base, last_round):
    """Trả (ok, reason_code). Không sửa state."""
    if action.kind == "buy":
        if not (0 < action.amount <= player.cash):
            return False, "INVALID_BUY_AMOUNT"
    elif action.kind in ("sell_local", "ship"):
        if player.rice <= 0:
            return False, "NO_INVENTORY"
        if action.kind == "ship" and r + T_base > last_round:
            return False, "SHIPMENT_CANNOT_ARRIVE_BEFORE_END"      # D6
    elif action.kind != "cancel":
        return False, "UNKNOWN_ACTION"
    return True, "OK"
