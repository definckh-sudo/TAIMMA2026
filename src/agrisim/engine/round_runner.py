"""Một vòng chơi theo 9 bước chuẩn (D1, ĐT 7.1). Mỗi bước tương ứng một hàm, dễ test riêng."""
from ..core import logistics, ledger
from ..domain.events import EventType
from ..domain.shipment import Shipment, ShipmentStatus
from .actions import validate
from .hints import make_hints

def step1_phase(game, r):
    ph = game.scenario.phase_of(r)
    if game.current_phase != ph.phase:                       # đổi phase -> shock đúng một lần
        before = game.pool.snapshot()
        if game.current_phase is not None and ph.pool_scale_on_enter != 1.0:
            game.pool.scale(ph.pool_scale_on_enter)
            game.log(r, EventType.POOL_DEPTH_SHOCK, "engine", {"s": ph.pool_scale_on_enter}, before, game.pool.snapshot())
        game.log(r, EventType.PHASE_CHANGE, "engine", {"from": game.current_phase, "to": ph.phase})
        game.current_phase = ph.phase
    return ph

def step2_true_state(game, r):
    tp = game.true_path
    game.log(r, EventType.MARKET_PRICE_UPDATE, "engine",
             {"P_asia": tp.asia.price(r), "eps_asia": tp.asia.epsilons[r],
              "P_europe": tp.europe.price(r), "eps_europe": tp.europe.epsilons[r]})
    if tp.port_event[r]:
        game.log(r, EventType.PORT_EVENT, "engine", {"event_id": f"port-r{r}"})

def step3_observation(game, r, ph):
    hints = make_hints(game.true_path, game.scenario, game.params, game.seed, game.replication, r)
    game.log(r, EventType.HINT_DISPLAYED, "engine", hints)
    return dict(round=r, phase=ph.phase, cash=game.player.cash, rice=game.player.rice,
                P_pool=game.pool.price, P_asia=game.true_path.asia.price(r),
                P_europe_now=game.true_path.europe.price(r), T_base=ph.T_base,
                price_trend=hints["price_trend_shown"], port_alert=hints["port_alert"],
                quote=game.pool.quote_buy_rice)

def step4_5_actions(game, r, ph, obs):
    for a in game.agent.decide(obs) if game.agent else []:
        ok, reason = validate(a, game.player, r, ph.T_base, game.params["game"]["rounds"])
        if not ok:
            game.log(r, EventType.ACTION_REJECTED, "player", {"kind": a.kind, "reason_code": reason}); continue
        if a.kind == "buy":
            before = game.pool.snapshot()
            out = game.pool.buy_rice(a.amount)
            game.player.cash -= a.amount
            game.player.add_position(a.amount, out, r)
            game.log(r, EventType.SWAP_CONFIRM, "player", {"usdg_in": a.amount, "rice_out": out}, before, game.pool.snapshot())
        elif a.kind == "sell_local":
            res = game.player.sell_local(a.amount, game.true_path.asia.price(r))
            game.log(r, EventType.LOCAL_SALE, "player", res)
        elif a.kind == "ship":
            sh = game.player.create_shipment(a.amount, r, ph, a.cold, game.next_id("SH"))
            p = game.params
            C_out = ledger.cash_out(sh.gross_usdg, ph.export_fee, p["route_asia_europe"]["c_ship"] * ph.ship_mult,
                                    sh.Q0, p["quality"]["C_cold"], sh.cold)      # công thức (2)
            game.player.cash -= C_out - sh.gross_usdg                            # C_acq đã trả lúc mua
            info = {k: v for k, v in vars(sh).items() if k not in ("applied_event_ids", "settlement")}
            game.log(r, EventType.SHIPMENT_CREATE, "player", info | {"C_out": C_out, "status": sh.status.value})

def step6_npc(game, r):
    if game.npc:
        res = game.npc.act(game.pool, game.true_path.asia.price(r))
        game.log(r, EventType.NPC_ARBITRAGE, "npc", res)

def step7_update_shipments(game, r):
    """Shipment tạo ở vòng t chỉ bắt đầu đếm từ vòng t+1 (D1); port event cộng dồn tối đa (D3)."""
    for sh in game.player.shipments:
        if sh.status != ShipmentStatus.IN_TRANSIT or sh.round_depart >= r:
            continue
        ev = f"port-r{r}"
        if game.true_path.port_event.get(r) and ev not in sh.applied_event_ids \
                and sh.port_delay < game.params["game"]["max_port_delay"]:
            sh.port_delay += 1; sh.applied_event_ids.add(ev)
        sh.elapsed_rounds += 1
        game.log(r, EventType.SHIPMENT_UPDATE, "engine",
                 {"shipment_id": sh.shipment_id, "elapsed": sh.elapsed_rounds, "port_delay": sh.port_delay})

def step8_settle(game, r):
    p, sc = game.params, game.scenario
    for sh in game.player.shipments:
        if sh.status != ShipmentStatus.IN_TRANSIT or sh.elapsed_rounds < sh.T_total:
            continue
        ph0 = sc.phases[sh.phase_depart - 1]
        lam_eff = logistics.lambda_effective(p["quality"]["lambda"], ph0.lambda_mult, sh.cold, p["quality"]["rho_cold"])
        s_T = logistics.survival(lam_eff, sh.elapsed_rounds)
        res = ledger.export_settlement(
            sh.gross_usdg, sh.Q_acquired, sh.Q0, s_T, game.true_path.europe.price(r),
            e=ph0.export_fee, c_ship=p["route_asia_europe"]["c_ship"] * ph0.ship_mult,
            C_cold=p["quality"]["C_cold"], cold=sh.cold, tau=p["route_asia_europe"]["tau"],
            s_min=p["quality"]["s_min"], r_c=p["capital"]["r_c"], T=sh.elapsed_rounds)
        res |= dict(shipment_id=sh.shipment_id, s_T=s_T, arrival_round=r)
        sh.settlement = res
        sh.status = ShipmentStatus.SETTLED if res["accepted"] else ShipmentStatus.REJECTED
        # C_out đã trừ lúc khởi hành; lúc đến cộng doanh thu, trừ thuế nhập khẩu và chi phí vốn
        game.player.cash += res["revenue"] - res["import_duty"] - res["capital_cost"]
        game.player.realized_profit += res["net_profit"]
        game.log(r, EventType.SHIPMENT_SETTLEMENT, "engine", res)

def step9_snapshot(game, r):
    game.log(r, EventType.ROUND_SNAPSHOT, "engine",
             {"cash": game.player.cash, "rice": game.player.rice, **game.pool.snapshot()})

def run_round(game, r, settlement_only=False):
    ph = step1_phase(game, r)
    step2_true_state(game, r)
    if not settlement_only:
        obs = step3_observation(game, r, ph)
        step4_5_actions(game, r, ph, obs)
        step6_npc(game, r)
    step7_update_shipments(game, r)
    step8_settle(game, r)
    step9_snapshot(game, r)
