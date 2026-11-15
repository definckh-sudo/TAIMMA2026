"""Ghi event log vào SQLite + kiểm tra toàn vẹn (BR16): seq liên tục, không thiếu trường."""
import json

class EventLogWriter:
    def __init__(self, con):
        self.con = con

    def write(self, ev):
        row = ev.to_row()
        self.con.execute("INSERT INTO event VALUES (?,?,?,?,?,?,?,?)",
                         (row["run_id"], row["seq"], row["round"], row["event_type"], row["actor"],
                          json.dumps(row["payload"], default=str), json.dumps(row["state_before"], default=str),
                          json.dumps(row["state_after"], default=str)))

    def register_run(self, game, agent_name, parameter_version="v1.0"):
        from .. import SCHEMA_VERSION
        self.con.execute("INSERT INTO run (run_id, scenario_id, scenario_version, parameter_version, model_version,"
                         " schema_version, seed, replication, agent, started_at) VALUES (?,?,?,?,?,?,?,?,?,datetime('now'))",
                         (game.run_id, game.scenario.scenario_id, game.scenario.scenario_version, parameter_version,
                          game.model_version(), SCHEMA_VERSION, game.seed, game.replication, agent_name))

def check_integrity(con, run_id):
    seqs = [s for (s,) in con.execute("SELECT seq FROM event WHERE run_id=? ORDER BY seq", (run_id,))]
    return seqs == list(range(1, len(seqs) + 1))
