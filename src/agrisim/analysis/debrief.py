"""Debrief cho người chơi: waterfall các khoản LC của từng shipment (Must) và chạy lại phản thực tế (Could, D18)."""

def lc_waterfall(settlement):
    keys = ["C_acq", "export_fee", "shipping", "cold_cost", "import_duty", "capital_cost"]
    return [(k, settlement.get(k, 0.0)) for k in keys] + [("revenue", settlement["revenue"]),
                                                          ("net_profit", settlement["net_profit"])]

def counterfactual(game_factory, strategies):
    """TODO (Could): chạy lại S1–S3 trên đúng seed/replication người chơi đã gặp."""
    raise NotImplementedError
