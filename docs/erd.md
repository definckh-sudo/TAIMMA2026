# ERD v0.1 (DRAFT) – chờ khóa cùng task "ERD" và GAME04

Nguồn trường: đặc tả 04/11 mục 9.1 (event log), GAME02 mục 2.3.6. Bảng SQL thật: `src/agrisim/storage/schema.sql`.

```mermaid
erDiagram
    RUN ||--o{ EVENT : ghi
    RUN ||--o{ MARKET_PRICE : sinh
    RUN ||--o{ SWAP : co
    RUN ||--o{ SHIPMENT : tao
    RUN ||--o{ HINT : hien_thi
    RUN ||--o{ ROUND_SNAPSHOT : chot
    RUN { text run_id PK  text scenario_id  text scenario_version  text parameter_version  text model_version  int seed  int replication  text agent }
    EVENT { text run_id FK  int seq  int round  text event_type  text actor  json payload  json state_before  json state_after }
    MARKET_PRICE { text run_id FK  int round  text market  real base_price  real phase_multiplier  real epsilon  real price }
    SWAP { text run_id FK  text tx_id  int round  text actor  real input_gross  real fee  real output  real P_spot  real P_exec }
    SHIPMENT { text run_id FK  text shipment_id  int round_depart  real Q0  int cold  int port_delay  real s_T  int accepted  real LC  real net_profit }
    HINT { text run_id FK  int round  text price_trend_shown  text price_trend_true  int port_alert  int false_positive  int false_negative }
    ROUND_SNAPSHOT { text run_id FK  int round  real cash  real rice  real X  real Y  real P_pool }
```

Việc cần chốt: kiểu dữ liệu và đơn vị từng trường (data dictionary), khóa ngoại hint → action kế tiếp (hint_id), bảng `local_sale` riêng hay để trong `event`.
