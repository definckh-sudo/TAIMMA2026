-- ERD v0.1 (DRAFT) cho AgriSim – chờ khóa cùng task "ERD" và GAME04 (data dictionary).
-- Quan hệ: run 1-n round_snapshot; run 1-n event; run 1-n shipment; run 1-n swap; run 1-n hint.
CREATE TABLE IF NOT EXISTS run (
    run_id TEXT PRIMARY KEY, scenario_id TEXT NOT NULL, scenario_version TEXT,
    parameter_version TEXT, model_version TEXT, schema_version TEXT,
    seed INTEGER NOT NULL, replication INTEGER NOT NULL, agent TEXT,
    started_at TEXT, status TEXT CHECK (status IN ('ok','invalid')) DEFAULT 'ok'
);
CREATE TABLE IF NOT EXISTS event (
    run_id TEXT REFERENCES run(run_id), seq INTEGER, round INTEGER, event_type TEXT, actor TEXT,
    payload_json TEXT, state_before_json TEXT, state_after_json TEXT,
    PRIMARY KEY (run_id, seq)
);
CREATE TABLE IF NOT EXISTS market_price (
    run_id TEXT REFERENCES run(run_id), round INTEGER, market TEXT, base_price REAL,
    phase_multiplier REAL, epsilon REAL, price REAL, PRIMARY KEY (run_id, round, market)
);
CREATE TABLE IF NOT EXISTS swap (
    run_id TEXT REFERENCES run(run_id), tx_id TEXT, round INTEGER, actor TEXT, direction TEXT,
    input_gross REAL, fee REAL, output REAL, X_before REAL, Y_before REAL, X_after REAL, Y_after REAL,
    P_spot REAL, P_exec REAL, price_impact REAL, PRIMARY KEY (run_id, tx_id)
);
CREATE TABLE IF NOT EXISTS shipment (
    run_id TEXT REFERENCES run(run_id), shipment_id TEXT, round_depart INTEGER, Q0 REAL,
    cold INTEGER, T_base INTEGER, port_delay INTEGER, arrival_round INTEGER, s_T REAL,
    accepted INTEGER, C_acq REAL, C_out REAL, import_duty REAL, capital_cost REAL, LC REAL,
    Q_sell REAL, revenue REAL, net_profit REAL, PRIMARY KEY (run_id, shipment_id)
);
CREATE TABLE IF NOT EXISTS hint (
    run_id TEXT REFERENCES run(run_id), round INTEGER, price_trend_shown TEXT, price_trend_true TEXT,
    price_hint_is_false INTEGER, port_alert INTEGER, false_positive INTEGER, false_negative INTEGER,
    PRIMARY KEY (run_id, round)
);
CREATE TABLE IF NOT EXISTS round_snapshot (
    run_id TEXT REFERENCES run(run_id), round INTEGER, cash REAL, rice REAL, X REAL, Y REAL,
    P_pool REAL, PRIMARY KEY (run_id, round)
);
