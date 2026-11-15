"""UT-03: NPC mua gạo khi pool rẻ, bán khi pool đắt, đứng yên trong threshold."""
from agrisim.core.npc import npc_trade

def test_buy_when_pool_cheap():
    d, amt, X, Y = npc_trade(1000, 10000, 14, 0.003, 0.3, 0.02, 0.10)
    assert d == "buy_rice" and Y / X > 10

def test_sell_when_pool_expensive():
    d, amt, X, Y = npc_trade(1000, 10000, 8, 0.003, 0.3, 0.02, 0.10)
    assert d == "sell_rice" and Y / X < 10

def test_no_op_inside_threshold():
    assert npc_trade(1000, 10000, 10.1, 0.003, 0.3, 0.02, 0.10)[0] == "no_op"
