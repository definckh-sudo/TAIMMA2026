"""PORT-01..03 và hint biên: tần suất port event ≈ p_port; hint không sửa trạng thái thật."""
import numpy as np
from agrisim.config import load_params, load_scenario
from agrisim.engine.scenario_engine import generate_true_path
from agrisim.engine.hints import make_hints

def test_port_frequency_close_to_config():
    sc, p = load_scenario("pandemic"), load_params()
    hits = [generate_true_path(sc, p, 3, rep).port_event[7] for rep in range(2000)]
    assert abs(np.mean(hits) - 0.30) < 0.03

def test_no_port_event_outside_window():
    tp = generate_true_path(load_scenario("pandemic"), load_params(), 3, 0)
    assert not any(tp.port_event[r] for r in (1, 2, 3, 4, 5, 10, 11, 12))

def test_hint_does_not_change_truth():
    sc, p = load_scenario("pandemic"), load_params()
    tp = generate_true_path(sc, p, 3, 0); before = dict(tp.europe.prices)
    make_hints(tp, sc, p, 3, 0, 5)
    assert tp.europe.prices == before
