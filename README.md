# AgriSim Global – lõi mô phỏng (không UI)

Một nguồn công thức duy nhất (`src/agrisim/core`) dùng chung cho: chạy ván chơi, Monte Carlo, test và đối chiếu Excel.

## Chạy nhanh
```bash
pip install -r requirements.txt
python -m pytest -q                       # 30 test: AMM, NPC, D7, luồng ván, tái lập, port/hint
python scripts/run_demo.py                # S1–S4 trên cùng diễn biến baseline và đại dịch
python scripts/run_game.py --strategy S3  # một ván 15 vòng, ghi SQLite + CSV event log
python scripts/run_mc.py --n 200          # Monte Carlo E1 + E2 (bỏ --n để chạy N = 10.000 theo config)
python scripts/run_d7_cases.py            # tình huống COVID theo D7, khớp excel/D7_COVID_tinh_huong.xlsx
```

## Phân lớp
`config/` (tham số, kịch bản, thí nghiệm) → `core/` (công thức) → `domain/` (đối tượng) → `engine/` (luồng 9 bước/vòng)
→ `agents/` (S1–S4) → `storage/` (SQLite, CSV) → `sim/` (Monte Carlo) → `analysis/` (bảng, hình, debrief).
Quy tắc: lớp dưới không import lớp trên; `sim/` và `scripts/` không tự viết công thức.

Xem `docs/open_items.md` cho các điểm còn chờ chốt.
