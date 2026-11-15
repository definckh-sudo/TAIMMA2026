"""GameSession: chạy trọn một ván 15 vòng (+ vòng settlement-only, D6) cho một tác tử."""
import uuid
from .. import MODEL_VERSION
from ..domain.pool import Pool
from ..domain.player import Player
from ..domain.npc_trader import NPCTrader
from ..domain.events import Event
from ..domain.shipment import ShipmentStatus
from .scenario_engine import generate_true_path
from .round_runner import run_round

class GameSession:
    def __init__(self, scenario, params, agent=None, seed=20261106, replication=0,
                 npc_enabled=True, start_cash=None, event_sink=None):
        self.scenario, self.params, self.agent = scenario, params, agent
        self.seed, self.replication = seed, replication
        self.run_id = f"{scenario.scenario_id}-{seed}-{replication}-{uuid.uuid4().hex[:6]}"
        a = params["amm"]
        self.pool = Pool(a["X0"], a["Y0"], a["f"])
        cash = params["player"]["start_cash"] if start_cash is None else start_cash
        self.start_cash = cash
        self.player = Player("P1", cash)
        n = params["npc"]
        self.npc = NPCTrader(n["alpha"], n["threshold"], n["cap_share_of_Y"]) if npc_enabled else None
        self.true_path = generate_true_path(scenario, params, seed, replication)
        self.current_phase = None
        self.events, self._seq, self._ids = [], 0, 0
        self.event_sink = event_sink            # vd. storage.event_log.EventLogWriter

    def next_id(self, prefix):
        self._ids += 1
        return f"{prefix}{self._ids:03d}"

    def log(self, r, etype, actor, payload=None, before=None, after=None):
        self._seq += 1
        ev = Event(self.run_id, r, self._seq, etype, actor, payload or {}, before or {}, after or {})
        self.events.append(ev)
        if self.event_sink:
            self.event_sink.write(ev)

    def run(self):
        last = self.params["game"]["rounds"]
        for r in range(1, last + 1):
            run_round(self, r)
        r = last
        while any(s.status == ShipmentStatus.IN_TRANSIT for s in self.player.shipments) \
                and r < self.true_path.last_round:
            r += 1
            run_round(self, r, settlement_only=True)
        return self.result()

    def result(self):
        last = self.params["game"]["rounds"]
        inv_value = self.player.rice * self.true_path.asia.price(last)        # D6: định giá tồn kho
        wealth = self.player.cash + inv_value
        ships = [s.settlement for s in self.player.shipments if s.settlement]
        return dict(run_id=self.run_id, scenario=self.scenario.scenario_id, seed=self.seed,
                    replication=self.replication, model_version=self.model_version(),
                    final_cash=self.player.cash, inventory_value=inv_value,
                    profit=wealth - self.start_cash, n_shipments=len(self.player.shipments),
                    rejected=sum(1 for s in ships if not s["accepted"]),
                    port_delay=sum(s.port_delay for s in self.player.shipments))

    @staticmethod
    def model_version():
        return MODEL_VERSION
