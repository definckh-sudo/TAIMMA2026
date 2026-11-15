# Các việc còn mở trước khi khóa code v1.0

| Hạng mục | File cần sửa | Trạng thái |
|---|---|---|
| Kịch bản COVID 15 vòng (task người trước) | `config/scenarios/pandemic.json` | DRAFT: đã có 3 giai đoạn theo D4/D5/D13–D15; còn sự kiện siết xuất khẩu vòng 5 (Proposal A3) chưa có tác động khóa |
| ERD / data dictionary (GAME04) | `src/agrisim/storage/schema.sql`, `docs/erd.md` | DRAFT v0.1 |
| λ theo giai đoạn khởi hành hay theo từng vòng | `engine/round_runner.py` (step8) | Đang dùng giai đoạn khởi hành (khớp bộ số của thầy) – cần nhóm xác nhận |
| Tương quan nhiễu giá Asia–Europe | `engine/scenario_engine.py` | Đang độc lập – PAR04 cần chốt |
| Baseline σ | `config/scenarios/baseline.json` | Đang 0,03 – cần chốt |
| E3 độ vững | `sim/experiments.py` | Khung, chưa chạy |
| Debrief phản thực tế (Could, D18) | `analysis/debrief.py` | Chưa làm |
