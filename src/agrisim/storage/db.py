import sqlite3
from pathlib import Path
SCHEMA = Path(__file__).with_name("schema.sql")

def connect(path="data/db/agrisim.db"):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(path)
    con.executescript(SCHEMA.read_text(encoding="utf-8"))
    return con
