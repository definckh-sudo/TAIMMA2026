"""S1–S4 (Feedback 3, mục 5.1). Mỗi chiến lược hành động một lần ở vòng quyết định t_d."""
from ..engine.actions import Action
from .base import Strategy

class S1Local(Strategy):
    name = "S1"
    def decide(self, obs):
        if obs["round"] != self.decision_round: return []
        return [Action("buy", self.budget), Action("sell_local", 0)]

class S2Export(Strategy):
    name = "S2"; cold = False
    def decide(self, obs):
        if obs["round"] != self.decision_round: return []
        return [Action("buy", self.budget), Action("ship", 0, cold=self.cold)]

class S3ExportCold(S2Export):
    name = "S3"; cold = True

class S4Adaptive(Strategy):
    """P_asia > P_pool·1,05 -> như S1; có port alert -> như S3; còn lại -> như S2."""
    name = "S4"
    def decide(self, obs):
        if obs["round"] != self.decision_round: return []
        if obs["P_asia"] > 1.05 * obs["P_pool"]:
            return [Action("buy", self.budget), Action("sell_local", 0)]
        return [Action("buy", self.budget), Action("ship", 0, cold=bool(obs["port_alert"]))]

STRATEGIES = {"S1": S1Local, "S2": S2Export, "S3": S3ExportCold, "S4": S4Adaptive}
