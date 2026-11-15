"""Sinh file Excel D7_COVID_tinh_huong.xlsx với công thức sống (đối chiếu cùng d7_covid_cases.py)."""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.comments import Comment
from openpyxl.utils import get_column_letter as L
from d7_covid_cases import CASES

FONT = "Arial"
BLUE = Font(name=FONT, color="0000FF")
BLACK = Font(name=FONT)
GREEN = Font(name=FONT, color="008000")
BOLD = Font(name=FONT, bold=True)
HEAD = Font(name=FONT, bold=True, color="FFFFFF")
HFILL = PatternFill("solid", fgColor="1F4E78")
SEC = PatternFill("solid", fgColor="DDEBF7")
KEY = PatternFill("solid", fgColor="FFF2CC")
thin = Side(style="thin", color="BFBFBF")
BOX = Border(left=thin, right=thin, top=thin, bottom=thin)
NUM, NUM4, PCT = '#,##0.00;(#,##0.00);"-"', "0.0000", "0.0%"

wb = Workbook()

# ---------------------------------------------------------------- 1. Tham_so
ws = wb.active; ws.title = "Tham_so"
ws["A1"] = "THAM SỐ CHUNG – Bảng tham số khóa v1.0 (Feedback 3, mục 3; giả định chung mục 4.1)"; ws["A1"].font = BOLD
hdr = ["Ký hiệu", "Tham số", "Giá trị", "Đơn vị", "Nguồn / ghi chú"]
for j, h in enumerate(hdr, 1):
    c = ws.cell(3, j, h); c.font = HEAD; c.fill = HFILL
params = [
    ("X", "Lượng gạo trong pool châu Á", 1000, "đơn vị gạo", "Proposal A5; Feedback 3 mục 4.1"),
    ("Y", "Lượng USDG trong pool châu Á", 10000, "USDG", "Proposal A5; Feedback 3 mục 4.1"),
    ("f", "Phí swap", 0, "tỷ lệ", "f = 0 như bộ số kiểm thử mục 4.1 (v1.0 dùng 0,3% cho Monte Carlo)"),
    ("ΔY_gross = B", "Ngân sách mua gạo", 1000, "USDG", "Feedback 3 mục 4.1 (B = 1.000)"),
    ("λ₀", "Tỷ lệ suy giảm nền", 0.01, "/vòng", "PAR06 – proxy"),
    ("ρ_cold", "Hiệu quả bảo quản (giảm λ)", 0.5, "tỷ lệ", "PAR07 – D9"),
    ("C_cold", "Chi phí bảo quản", 0.4, "USDG/đơn vị", "PAR07 – D9"),
    ("τ", "Thuế nhập khẩu trên trị giá CIF", 0.08, "tỷ lệ", "PAR10 – D7"),
    ("s_min", "Ngưỡng tỷ lệ còn bán được", 0.85, "tỷ lệ", "PAR09 – D8"),
    ("r_c", "Chi phí vốn mỗi vòng trên C_out", 0.002, "/vòng", "PAR11 (≈10%/năm nếu 1 vòng = 1 tuần)"),
]
for i, (sym, name, val, unit, src) in enumerate(params, 4):
    for j, v in enumerate((sym, name, val, unit, src), 1):
        c = ws.cell(i, j, v); c.font = BLUE if j == 3 else BLACK; c.border = BOX
    ws.cell(i, 3).fill = KEY
    ws.cell(i, 3).number_format = PCT if unit in ("tỷ lệ", "/vòng") else "#,##0.00"
ws["C9"].number_format = ws["C13"].number_format = "0.00%"
for col, w in zip("ABCDE", (16, 36, 12, 14, 64)):
    ws.column_dimensions[col].width = w
P = {k: f"Tham_so!$C${r}" for k, r in
     zip(("X", "Y", "f", "B", "lam0", "rho", "Ccold", "tau", "smin", "rc"), range(4, 14))}

# ---------------------------------------------------------------- 2. Tinh_toan
tt = wb.create_sheet("Tinh_toan")
tt["A1"] = "TÍNH TOÁN TỪNG BƯỚC THEO SỔ CHI PHÍ D7 – mỗi cột là một tình huống × lựa chọn bảo quản"; tt["A1"].font = BOLD
tt["A2"] = "Chữ xanh dương = đầu vào có thể sửa; chữ đen = công thức; chữ xanh lá = liên kết sang sheet Tham_so."
tt["A2"].font = Font(name=FONT, italic=True)
cols = [(c, cold) for c in CASES for cold in (0, 1)]
FIRST = 4  # cột D trở đi
rows = {}
layout = [
    ("sec", "A. ĐẦU VÀO TÌNH HUỐNG"),
    ("code", "Mã tình huống", "", "", "in"),
    ("name", "Tên tình huống", "", "", "in"),
    ("cold", "Bảo quản (1 = có, 0 = không)", "1[cold]", "", "in"),
    ("PA", "Giá thị trường châu Á tại vòng quyết định", "P_A", "USDG/đv", "in"),
    ("PE", "Giá châu Âu tại vòng hàng đến", "P_E,arr", "USDG/đv", "in"),
    ("lm", "Hệ số λ theo giai đoạn khởi hành", "M_λ", "lần", "in"),
    ("Tb", "Thời gian vận chuyển cơ sở", "T_base", "vòng", "in"),
    ("dl", "Số vòng tắc cảng cộng dồn", "Σδ_port", "vòng", "in"),
    ("cs", "Cước vận chuyển", "c_ship", "USDG/đv", "in"),
    ("e", "Phí xuất khẩu trên giá vốn", "e", "tỷ lệ", "in"),
    ("sh", "Tỷ lệ lượng gạo đưa lên tàu", "Q₀/Q_acq", "tỷ lệ", "in"),
    ("sec", "B. BIẾN TRUNG GIAN"),
    ("Qa", "Lượng gạo mua được từ pool (EQ03)", "Q_acq", "đv gạo", "=X*(1-f)*B/(Y+(1-f)*B)"),
    ("Q0", "Lượng gạo đưa lên tàu", "Q₀", "đv gạo", "=sh*Qa"),
    ("T", "Số vòng hàng trên đường", "T_elapsed", "vòng", "=Tb+dl"),
    ("le", "Tỷ lệ suy giảm hiệu dụng (EQ11)", "λ_eff", "/vòng", "=lam0*lm*(1-rho*cold)"),
    ("sT", "Tỷ lệ hàng còn bán được (EQ10)", "s_T", "tỷ lệ", "=(1-le)^T"),
    ("acc", "Lô hàng được nhận (EQ12)", "1[accepted]", "0/1", "=IF(sT>=smin,1,0)"),
    ("sec", "C. NĂM CÔNG THỨC D7"),
    ("Cacq", "(1) Giá vốn lô hàng C_acq = ΔY_gross × Q₀ / Q_acq", "C_acq", "USDG", "=B*Q0/Qa"),
    ("fee", "    – Phí xuất khẩu C_acq × e", "", "USDG", "=Cacq*e"),
    ("ship", "    – Cước c_ship × Q₀", "", "USDG", "=cs*Q0"),
    ("ccost", "    – Bảo quản C_cold × Q₀ × 1[cold]", "", "USDG", "=Ccold*Q0*cold"),
    ("Cout", "(2) Tiền chi lúc khởi hành C_out = C_acq(1+e) + c_ship·Q₀ + C_cold·Q₀·1[cold]", "C_out", "USDG", "=Cacq*(1+e)+cs*Q0+Ccold*Q0*cold"),
    ("duty", "    – Thuế nhập khẩu τ(C_acq + c_ship·Q₀)·1[accepted]", "", "USDG", "=tau*(Cacq+cs*Q0)*acc"),
    ("cap", "    – Chi phí vốn r_c · C_out · T", "", "USDG", "=rc*Cout*T"),
    ("LC", "(3) Landed cost LC = C_out + thuế + chi phí vốn", "LC", "USDG", "=Cout+duty+cap"),
    ("Qs", "(4) Lượng bán được Q_sell = Q₀·s_T nếu s_T ≥ s_min, ngược lại 0", "Q_sell", "đv gạo", "=IF(sT>=smin,Q0*sT,0)"),
    ("rev", "    – Doanh thu P_E,arr × Q_sell", "", "USDG", "=PE*Qs"),
    ("pi", "(5) Lợi nhuận ròng π = P_E,arr·Q_sell − LC", "π", "USDG", "=rev-LC"),
    ("sec", "D. CHỈ SỐ ĐỂ SO SÁNH"),
    ("pi0", "π nếu r_c = 0 (để đối chiếu bảng mục 4.1)", "π|r_c=0", "USDG", "=rev-Cout-duty"),
    ("mg", "Biên lợi nhuận trên giá vốn", "π / C_acq", "%", "=pi/Cacq"),
    ("spq", "Lượng gạo mất (hư hỏng hoặc bị từ chối)", "Q₀ − Q_sell", "đv gạo", "=Q0-Qs"),
    ("spv", "Giá trị gạo mất tính theo giá châu Âu", "", "USDG", "=PE*(Q0-Qs)"),
    ("pil", "Lãi phần không xuất, bán tại châu Á (TH5)", "", "USDG", "=PA*(Qa-Q0)-B*(Qa-Q0)/Qa"),
    ("pit", "Tổng lãi cả lô mua", "", "USDG", "=pi+pil"),
    ("s1", "Tham chiếu S1: bán cả lô tại châu Á", "π_S1", "USDG", "=PA*Qa-B"),
]
head = ["Bước", "Ký hiệu", "Đơn vị"]
for j, h in enumerate(head, 1):
    c = tt.cell(3, j, h); c.font = HEAD; c.fill = HFILL
for k, (case, cold) in enumerate(cols):
    c = tt.cell(3, FIRST + k, f"{case[0]}-{'có BQ' if cold else 'không BQ'}"); c.font = HEAD; c.fill = HFILL
    c.alignment = Alignment(horizontal="center")
r = 4
for item in layout:
    if item[0] == "sec":
        tt.cell(r, 1, item[1]).font = BOLD
        for j in range(1, FIRST + len(cols)):
            tt.cell(r, j).fill = SEC
        r += 1; continue
    rows[item[0]] = r; r += 1

import re
def to_excel(expr, col):
    def sub(m):
        t = m.group(0)
        if t in rows:
            return f"{col}{rows[t]}"
        if t in P:
            return P[t]
        return t
    return re.sub(r"[A-Za-z_][A-Za-z0-9_]*", lambda m: sub(m) if m.group(0) != "IF" else "IF", expr)

for item in layout:
    if item[0] == "sec":
        continue
    key, label, sym, unit, spec = item
    rr = rows[key]
    tt.cell(rr, 1, label).font = BOLD if label.startswith("(") else BLACK
    tt.cell(rr, 2, sym).font = BLACK; tt.cell(rr, 3, unit).font = BLACK
    for k, (case, cold) in enumerate(cols):
        col = L(FIRST + k); c = tt[f"{col}{rr}"]; c.border = BOX
        if spec == "in":
            vals = dict(code=case[0], name=case[1], cold=cold, PA=case[2], PE=case[3], lm=case[4],
                        Tb=case[5], dl=case[6], cs=case[7], e=case[8], sh=case[9])
            c.value = vals[key]; c.font = BLUE
        else:
            c.value = to_excel(spec, col); c.font = GREEN if any(p in c.value for p in P.values()) and key in ("Qa", "le", "Cacq", "s1") else BLACK
        if key in ("e", "sh", "mg"):
            c.number_format = PCT
        elif key in ("lm", "le", "sT", "Qa", "Q0", "Qs", "spq"):
            c.number_format = NUM4
        elif key in ("Tb", "dl", "T", "acc", "cold"):
            c.number_format = "0"
        elif key not in ("code", "name"):
            c.number_format = NUM
        if key in ("pi", "LC", "Cout", "Cacq", "Qs"):
            c.fill = KEY; c.font = Font(name=FONT, bold=True, color=c.font.color.rgb if c.font.color else None)
        c.alignment = Alignment(horizontal="center", wrap_text=(key == "name"))
tt.row_dimensions[rows["name"]].height = 45
tt.column_dimensions["A"].width = 70; tt.column_dimensions["B"].width = 13; tt.column_dimensions["C"].width = 10
for k in range(len(cols)):
    tt.column_dimensions[L(FIRST + k)].width = 15
tt.freeze_panes = "D4"
tt.cell(rows["PE"], 1).comment = Comment("TH0: 13; TH1–TH3, TH5: 18 (giữ như A7 và bộ số mục 4.1); TH4: 13 × 1,15 = 14,95 (hệ số GĐ3, PAR03).", "Claude")
tt.cell(rows["Tb"], 1).comment = Comment("D5: T_base = 6 / 10 / 8 vòng theo giai đoạn khởi hành GĐ1 / GĐ2 / GĐ3.", "Claude")
tt.cell(rows["dl"], 1).comment = Comment("D3: mỗi port event cộng 1 vòng, cộng dồn tối đa 4 vòng (vòng 6–9, p = 0,30).", "Claude")

# ---------------------------------------------------------------- 3. So_sanh
ss = wb.create_sheet("So_sanh")
ss["A1"] = "SO SÁNH CÁC TÌNH HUỐNG (liên kết từ Tinh_toan, r_c = 0,2%/vòng)"; ss["A1"].font = BOLD
sh = ["Tình huống", "Bảo quản", "T (vòng)", "s_T", "Nhận hàng", "C_out (USDG)", "LC (USDG)",
      "Doanh thu (USDG)", "π (USDG)", "π / C_acq", "Δπ so với TH0 cùng lựa chọn BQ (USDG)",
      "Giá trị gạo mất (USDG)", "π_S1 bán nội địa (USDG)", "Chiến lược tốt nhất"]
for j, h in enumerate(sh, 1):
    c = ss.cell(3, j, h); c.font = HEAD; c.fill = HFILL; c.alignment = Alignment(wrap_text=True, horizontal="center")
src = [("name", None), ("cold", "0"), ("T", "0"), ("sT", NUM4), ("acc", "0"), ("Cout", NUM), ("LC", NUM),
       ("rev", NUM), ("pi", NUM), ("mg", PCT)]
for k, (case, cold) in enumerate(cols):
    rr = 4 + k; col = L(FIRST + k)
    for j, (key, fmt) in enumerate(src, 1):
        c = ss.cell(rr, j, f"=Tinh_toan!{col}{rows[key]}"); c.font = GREEN; c.border = BOX
        if fmt: c.number_format = fmt
    base_col = L(FIRST + cold)  # TH0 cùng lựa chọn bảo quản
    ss.cell(rr, 11, f"=Tinh_toan!{col}{rows['pi']}-Tinh_toan!{base_col}{rows['pi']}").number_format = NUM
    ss.cell(rr, 12, f"=Tinh_toan!{col}{rows['spv']}").number_format = NUM
    ss.cell(rr, 13, f"=Tinh_toan!{col}{rows['s1']}").number_format = NUM
    ss.cell(rr, 14, f'=IF(Tinh_toan!{col}{rows["s1"]}>Tinh_toan!{col}{rows["pit"]},"S1 bán nội địa","Xuất khẩu")')
    for j in (11, 12, 13, 14):
        ss.cell(rr, j).font = GREEN if j < 14 else BLACK; ss.cell(rr, j).border = BOX
    ss.cell(rr, 9).fill = KEY
for col, w in zip("ABCDEFGHIJKLMN", (44, 9, 9, 9, 10, 13, 13, 14, 13, 10, 18, 14, 14, 18)):
    ss.column_dimensions[col].width = w
ss.row_dimensions[3].height = 48
ss.cell(17, 1, "Ghi chú: TH5 xuất 1/2 lô nên cột 'Chiến lược tốt nhất' so S1 với tổng lãi cả lô (phần xuất + phần bán nội địa).").font = Font(name=FONT, italic=True)

# ---------------------------------------------------------------- 4. Doi_chieu
dc = wb.create_sheet("Doi_chieu")
dc["A1"] = "ĐỐI CHIẾU VỚI BỘ SỐ KIỂM THỬ CỦA THẦY (Feedback 3, mục 4.1 – r_c = 0, sai số cho phép ±0,01)"; dc["A1"].font = BOLD
dh = ["Dòng trong bảng 4.1 của thầy", "Cột trong Tinh_toan", "Giá trị thầy (USDG)", "Excel tính (USDG)", "Chênh lệch", "Đạt?"]
for j, h in enumerate(dh, 1):
    c = dc.cell(3, j, h); c.font = HEAD; c.fill = HFILL
checks = [("Baseline – S2 xuất, không bảo quản", 0, 0, "pi0", -16.43),
          ("Baseline – S3 xuất, có bảo quản", 0, 1, "pi0", -18.65),
          ("Cú sốc – S1 bán nội địa", 2, 0, "s1", 272.73),
          ("Baseline – S1 bán nội địa", 0, 0, "s1", -90.91),
          ("Cú sốc – S2, không trễ", 2, 0, "pi0", 54.10),
          ("Cú sốc – S2, 1 port delay (từ chối)", 4, 0, "pi0", -1263.64),
          ("Cú sốc – S3, không trễ", 2, 1, "pi0", 128.61),
          ("Cú sốc – S3, 1 port delay", 4, 1, "pi0", 117.22),
          ("Cú sốc – S3, 3 port delay", 6, 1, "pi0", 94.71),
          ("Ví dụ chi tiết: S2 cú sốc, r_c = 0,2% (π = 28,83)", 2, 0, "pi", 28.83),
          ("Ví dụ chi tiết: chi phí vốn 25,27", 2, 0, "cap", 25.27),
          ("Ví dụ chi tiết: LC = 1.352,73 khi r_c = 0", 2, 0, None, 1352.73)]
for i, (lab, idx, cold, key, val) in enumerate(checks, 4):
    col = L(FIRST + idx + cold)
    dc.cell(i, 1, lab); dc.cell(i, 2, f"{col} ({cols[idx + cold][0][0]})")
    dc.cell(i, 3, val).font = BLUE
    f = f"=Tinh_toan!{col}{rows[key]}" if key else f"=Tinh_toan!{col}{rows['Cout']}+Tinh_toan!{col}{rows['duty']}"
    dc.cell(i, 4, f).font = GREEN
    dc.cell(i, 5, f"=D{i}-C{i}")
    dc.cell(i, 6, f'=IF(ABS(E{i})<=0.01,"Đạt","KHÔNG ĐẠT")')
    for j in range(3, 6):
        dc.cell(i, j).number_format = NUM
    for j in range(1, 7):
        dc.cell(i, j).border = BOX
for col, w in zip("ABCDEF", (52, 18, 18, 18, 12, 12)):
    dc.column_dimensions[col].width = w

# ---------------------------------------------------------------- 5. Ghi_chu
gc = wb.create_sheet("Ghi_chu")
notes = [
    "CÁCH DÙNG FILE",
    "1. Sửa ô chữ xanh dương (tham số chung ở Tham_so, đầu vào tình huống ở Tinh_toan dòng 5–15); mọi kết quả tự tính lại.",
    "2. Sheet Doi_chieu phải hiện 'Đạt' ở mọi dòng khi giữ nguyên tham số gốc; nếu đổi tham số, bảng đối chiếu sẽ lệch là bình thường.",
    "3. Bộ code d7_covid_cases.py tính cùng các công thức; d7_results.csv là đầu ra để so từng ô.",
    "",
    "NĂM CÔNG THỨC D7 (Feedback 3, mục 2.2)",
    "(1) C_acq = ΔY_gross × Q₀ / Q_acquired",
    "(2) C_out = C_acq·(1 + e) + c_ship·Q₀ + C_cold·Q₀·1[cold]",
    "(3) LC = C_out + τ·(C_acq + c_ship·Q₀)·1[accepted] + r_c·C_out·T_elapsed",
    "(4) Q_sell = Q₀·s_T nếu s_T ≥ s_min; Q_sell = 0 nếu ngược lại",
    "(5) π = P_E,arr·Q_sell − LC",
    "Công thức phụ trợ: Q_acq = X·(1−f)·ΔY/(Y + (1−f)·ΔY) (EQ03); λ_eff = λ₀·M_λ·(1 − ρ_cold·1[cold]) (EQ11); s_T = (1 − λ_eff)^T (EQ10).",
    "",
    "GIẢ ĐỊNH CỦA CÁC TÌNH HUỐNG",
    "– Giá pool đứng ở 10 lúc mua (NPC tắt, f = 0), đúng giả định chung của bộ số kiểm thử mục 4.1.",
    "– P_E giữ cố định là đầu vào (13 trước dịch, 18 trong cú sốc như A7; 14,95 trong phục hồi = 13 × 1,15).",
    "– TH4 (phục hồi): T_base = 8, c_ship = 0,5 × 1,60 = 0,80, λ × 1,2, e = 5%, P_A = 10 × 1,15 = 11,5 (PAR03, D5, PAR10).",
    "– TH5: tình huống bổ sung để minh họa công thức (1) khi chỉ xuất một phần lô; phần còn lại bán tại châu Á theo quy tắc phân bổ giá vốn (đặc tả 04/11, mục 5.7).",
    "– Mọi tham số Thiết kế/Proxy là lựa chọn sư phạm, không phải số liệu thực tế của ngành gạo.",
]
for i, t in enumerate(notes, 1):
    gc.cell(i, 1, t).font = BOLD if t.isupper() or t.startswith("NĂM") else BLACK
gc.column_dimensions["A"].width = 140

for sheet in wb.worksheets:
    for row in sheet.iter_rows():
        for c in row:
            if c.font and c.font.name != FONT:
                c.font = Font(name=FONT, bold=c.font.bold, italic=c.font.italic, color=c.font.color)
wb.save("D7_COVID_tinh_huong.xlsx")
print("saved")
