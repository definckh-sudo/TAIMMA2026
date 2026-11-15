class Strategy:
    """Giao diện chung: decide(observation) -> list[Action]. Chỉ dùng thông tin hiển thị, không dùng trạng thái thật."""
    name = "base"

    def __init__(self, budget=500.0, decision_round=5):
        self.budget, self.decision_round = budget, decision_round

    def decide(self, obs):
        raise NotImplementedError
