"""Seed và random stream tách biệt (ĐT 6.7): seed_stream = H(seed0, scenario, replication, stream).
Thêm stream mới không làm đổi chuỗi giá/port event cũ; các chiến lược dùng chung draws (CRN)."""
import zlib
import numpy as np

STREAMS = ("market_price", "port_event", "hint_accuracy", "hint_style")

def _stable_id(text):
    return zlib.crc32(text.encode("utf-8"))      # ổn định giữa các lần chạy (không dùng hash())

def stream(seed0, scenario_id, replication, name):
    assert name in STREAMS, f"stream lạ: {name}"
    ss = np.random.SeedSequence([seed0, _stable_id(scenario_id), replication, _stable_id(name)])
    return np.random.default_rng(ss)
