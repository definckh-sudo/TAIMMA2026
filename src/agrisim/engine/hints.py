"""Hint hướng về tương lai (D13) – chỉ đọc trạng thái thật, KHÔNG được sửa nó (ĐT 3.2)."""
from .rng import stream

def make_hints(true_path, scenario, params, seed0, replication, r):
    ph = scenario.phase_of(r)
    g_acc = stream(seed0, scenario.scenario_id, replication, "hint_accuracy")
    g_acc = [g_acc.random(2) for _ in range(r)][-1]           # draw riêng cho vòng r, tái lập được
    band = params["hint"]["price_trend_band"]
    eta = min(r + ph.T_base, true_path.last_round)
    change = true_path.europe.price(eta) / true_path.europe.price(r) - 1
    truth = "up" if change > band else ("down" if change < -band else "stable")
    is_false = g_acc[0] < ph.p_false_price
    shown = {"up": "down", "down": "up", "stable": "up"}[truth] if is_false else truth
    nxt = min(r + 1, true_path.last_round)
    event_next = true_path.port_event[nxt]
    p_fn, p_fp = params["hint"]["port_alert_fn"], params["hint"]["port_alert_fp"]
    alert = (g_acc[1] >= p_fn) if event_next else (g_acc[1] < p_fp)
    return dict(price_trend_shown=shown, price_trend_true=truth, price_hint_is_false=is_false,
                port_alert=alert, port_event_next_true=event_next,
                false_positive=alert and not event_next, false_negative=(not alert) and event_next)
