#!/usr/bin/env python3
"""Generate the 3-firm synthetic document corpus + hand-computed ground truth.

Outputs (data/mock_corpus/ — gitignored, regenerate at will):
    {firm_a,firm_b,firm_c}/
        bills/taipower_YYYY_MM.pdf|.png      12 monthly Taipower TOU bills (高壓三段式)
        invoices/*.xml                       MIG 4.0 F0401-style B2B e-invoices (steel/gas/chemicals)
        invoices/*.pdf|.png                  rendered 電子發票證明聯 for the VLM path
        production_log.csv|.pdf              per-CN-code monthly tonnes + machine table
        firm.json                            installation identity (LINE-onboarding stand-in)
    ground_truth.json                        per-firm expected extractions + hand-computed SEE

Scenario design (docs/archive/10 §2A input priority — steel precursor dominates):
    firm_a  carbon-steel screws only, 1 process, NO mill EPD -> precursor from CBAM
            default (Taiwan CN 7213 + 2026 mark-up). The common case.
    firm_b  carbon + stainless lines, 2 processes sharing one meter & furnace ->
            allocation by machine-power x run-hours priors (the OR-Tools case).
    firm_c  same shape as firm_a but WITH a CSC mill EPD -> actual precursor SEE.

Determination period: calendar year 2026 (per-product-per-YEAR, never per-shipment).
All ground-truth math mirrors the Commission's screws & nuts answer key chain:
    SEE_dir(good) = DirEm(p)/AL(p) + sum_i m_i/AL(p) * SEE_dir(prec_i)
    SEE_ind(good) = Elec(p)*EF/AL(p) + sum_i m_i/AL(p) * SEE_ind(prec_i)   [recorded, NOT in CN 7318 certificate]
"""
from __future__ import annotations

import json
import random
from datetime import date
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "data" / "mock_corpus"
PERIOD_YEAR = 2026

# Traditional-Chinese font: prefer a full-coverage system TTF (STSong-Light and
# friends are Simplified-only CID fonts and drop Traditional glyphs).
_TTF_CANDIDATES = [
    "/Library/Fonts/Arial Unicode.ttf",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
]
ZH = None
for _p in _TTF_CANDIDATES:
    if Path(_p).exists():
        from reportlab.pdfbase.ttfonts import TTFont

        pdfmetrics.registerFont(TTFont("ZH-TC", _p))
        ZH = "ZH-TC"
        break
if ZH is None:  # CID fallback (Traditional Chinese)
    from reportlab.pdfbase.cidfonts import UnicodeCIDFont

    pdfmetrics.registerFont(UnicodeCIDFont("MSung-Light"))
    ZH = "MSung-Light"

from carbonpass.rules.gridef import load_grid_ef

GRID_EF = load_grid_ef().kgco2e_per_kwh   # same source as the engine — GT cannot diverge
NG_NCV_GJ_PER_KNM3 = 38.5  # GJ per 1000 Nm3 natural gas
NG_EF_TCO2_PER_TJ = 56.1   # IPCC / template example value

# CBAM default values (data/cbam_official/default_values.xlsx), "2026 (including mark-up)"
# column — the +10% year. Ground truth is computed independently of the engine on purpose,
# so these are transcribed from the workbook rather than looked up.
#
# Carbon wire rod: Taiwan sheet, CN 7213 (base 2.297829146).
DEFAULT_SEE_WIRE_ROD_7213_2026 = 2.5276120606
# Stainless wire rod: CN 7221. Taiwan's sheet has NO 7221 value — the row reads "see below"
# and nothing is below it (only Taiwan, Thailand and Vietnam have this hole among the 33
# full-book countries). So the Annex I "Other countries and territories" table applies
# (Q&A p.37 §4.25) — base 4.82, the average of the ten highest-intensity exporters.
DEFAULT_SEE_WIRE_ROD_7221_2026 = 5.302

# TOU rates, NT$/kWh — single source of truth in the scheduler module
from carbonpass.scheduler.tariffs import RATES  # noqa: E402


# ---------------------------------------------------------------------------
# Firm specifications (all quantities ANNUAL; monthly docs are derived shares)
# ---------------------------------------------------------------------------
FIRMS = {
    "firm_a": {
        "seed": 41,
        "identity": {
            "name_zh": "鋼旭精密工業股份有限公司",
            "name_en": "Gang Xu Precision Industry Co., Ltd.",
            "ban": "24567890",  # 統一編號
            "street": "No. 88, Bengong 1st Rd., Gangshan Dist.",
            "city": "Kaohsiung City",
            "post_code": "820",
            "country": "Taiwan",
            "unlocode": "TW KHH",
            "latitude": "22.7972°",
            "longitude": "120.2617°",
            "economic_activity": "Iron & steel production",
            "electricity_no": "07-12-3456-78-9",
            "contract_capacity_kw": 499,
        },
        "processes": [
            {
                "name": "Carbon steel screws and nuts",
                "cn_code": "73181542",
                "invoice_name": "Hex bolts M6-M20 Gr8.8",
                "production_t": 3000.0,
            },
        ],
        "precursors": [
            {
                "name": "Carbon steel wire rod",
                "grade": "SAE1008",
                "cn_code_precursor": "7213",
                "country": "TW",
                "supplier": "中鋼碳素鋼股份有限公司",
                "supplier_ban": "23204101",
                "purchased_t": 3600.0,
                "consumed_t": {"Carbon steel screws and nuts": 3300.0},
                "consumed_other_t": 300.0,
                "unit_price_ntd_per_kg": 24.5,
                "epd": None,  # -> CBAM default value (the common case)
            },
        ],
        "natural_gas_knm3": 200.0,   # 1000 Nm3 / year, heat-treatment furnaces
        "gas_supplier": {"name": "欣高石油氣股份有限公司", "ban": "76002807",
                         "unit_price_ntd_per_m3": 17.8},
        "electricity_mwh": 600.0,
        "plating_chemicals_ntd": 1_860_000,  # non-emission line items (noise for the parser)
        "machines": [
            {"name_zh": "抽線機", "name_en": "Wire drawing", "kw": 55, "hours": 4200, "process": "Carbon steel screws and nuts"},
            {"name_zh": "冷鍛成型機", "name_en": "Cold former", "kw": 90, "hours": 4400, "process": "Carbon steel screws and nuts"},
            {"name_zh": "搓牙機", "name_en": "Thread roller", "kw": 30, "hours": 4400, "process": "Carbon steel screws and nuts"},
            {"name_zh": "連續式熱處理爐", "name_en": "Heat-treatment furnace", "kw": 65, "hours": 5800, "process": "Carbon steel screws and nuts"},
        ],
    },
    "firm_b": {
        "seed": 42,
        "identity": {
            "name_zh": "隆祥螺絲工業股份有限公司",
            "name_en": "Long Xiang Fastener Industry Co., Ltd.",
            "ban": "86753091",
            "street": "No. 152, Luke 3rd Rd., Luzhu Dist.",
            "city": "Kaohsiung City",
            "post_code": "821",
            "country": "Taiwan",
            "unlocode": "TW KHH",
            "latitude": "22.8461°",
            "longitude": "120.2755°",
            "economic_activity": "Iron & steel production",
            "electricity_no": "07-31-9876-54-3",
            "contract_capacity_kw": 800,
        },
        "processes": [
            {
                "name": "Carbon steel screws and nuts",
                "cn_code": "73181542",
                "invoice_name": "Machine screws M4-M12",
                "production_t": 4200.0,
            },
            {
                "name": "Stainless steel screws and nuts",
                "cn_code": "73181535",
                "invoice_name": "SUS304 hex cap screws",
                "production_t": 1300.0,
            },
        ],
        "precursors": [
            {
                "name": "Carbon steel wire rod",
                "grade": "SAE1010",
                "cn_code_precursor": "7213",
                "country": "TW",
                "supplier": "中鋼碳素鋼股份有限公司",
                "supplier_ban": "23204101",
                "purchased_t": 4650.0,
                "consumed_t": {"Carbon steel screws and nuts": 4650.0},
                "consumed_other_t": 0.0,
                "unit_price_ntd_per_kg": 24.9,
                "epd": None,
            },
            {
                "name": "Stainless steel wire rod",
                "grade": "SUS304",
                "cn_code_precursor": "7221",
                "country": "TW",
                "supplier": "唐榮鐵工廠股份有限公司",
                "supplier_ban": "85510258",
                "purchased_t": 1440.0,
                "consumed_t": {"Stainless steel screws and nuts": 1440.0},
                "consumed_other_t": 0.0,
                "unit_price_ntd_per_kg": 96.0,
                "epd": None,
            },
        ],
        "natural_gas_knm3": 330.0,
        "gas_supplier": {"name": "欣雄天然氣股份有限公司", "ban": "80234561",
                         "unit_price_ntd_per_m3": 18.1},
        "electricity_mwh": 1265.0,
        "plating_chemicals_ntd": 2_540_000,
        # Shared meter & furnace: allocation must split by kW x hours priors.
        "machines": [
            {"name_zh": "抽線機", "name_en": "Wire drawing", "kw": 75, "hours": 4600, "process": "Carbon steel screws and nuts"},
            {"name_zh": "冷鍛成型機#1", "name_en": "Cold former 1", "kw": 110, "hours": 4800, "process": "Carbon steel screws and nuts"},
            {"name_zh": "搓牙機", "name_en": "Thread roller", "kw": 37, "hours": 4800, "process": "Carbon steel screws and nuts"},
            {"name_zh": "冷鍛成型機#2", "name_en": "Cold former 2 (SUS)", "kw": 132, "hours": 2400, "process": "Stainless steel screws and nuts"},
            {"name_zh": "搓牙機#2", "name_en": "Thread roller 2 (SUS)", "kw": 30, "hours": 2400, "process": "Stainless steel screws and nuts"},
            {"name_zh": "連續式熱處理爐", "name_en": "Heat-treatment furnace", "kw": 80, "hours": 6000, "process": "shared"},
        ],
        # Ground-truth allocation of the shared gas furnace between the two
        # processes: by heat demand ~ production tonnes.
        "gas_split_by": "production_t",
    },
    "firm_c": {
        "seed": 43,
        "identity": {
            "name_zh": "宏茂金屬工業股份有限公司",
            "name_en": "Hong Mao Metal Industry Co., Ltd.",
            "ban": "53127946",
            "street": "No. 21, Gangshan N. Rd., Gangshan Dist.",
            "city": "Kaohsiung City",
            "post_code": "820",
            "country": "Taiwan",
            "unlocode": "TW KHH",
            "latitude": "22.7883°",
            "longitude": "120.2951°",
            "economic_activity": "Iron & steel production",
            "electricity_no": "07-55-2468-13-5",
            "contract_capacity_kw": 350,
        },
        "processes": [
            {
                "name": "Carbon steel screws and nuts",
                "cn_code": "73181588",
                "invoice_name": "Flange bolts M8-M16",
                "production_t": 1800.0,
            },
        ],
        "precursors": [
            {
                "name": "Carbon steel wire rod",
                "grade": "CH1T",
                "cn_code_precursor": "7213",
                "country": "TW",
                "supplier": "中鋼碳素鋼股份有限公司",
                "supplier_ban": "23204101",
                "purchased_t": 2000.0,
                "consumed_t": {"Carbon steel screws and nuts": 1980.0},
                "consumed_other_t": 20.0,
                "unit_price_ntd_per_kg": 26.0,
                # Mill EPD supplied -> ACTUAL precursor SEE (the good case)
                "epd": {
                    "document": "CSC_EPD_wire_rod_2025.pdf (mill environmental product declaration)",
                    "see_direct": 1.85,
                    "spec_electricity_mwh_per_t": 0.42,
                    # the EPD document's OWN stated factor: a 2025-issued EPD cites the
                    # then-current 2024 grid EF — document data, not the engine's EF
                    "electricity_ef": 0.474,
                },
            },
        ],
        "natural_gas_knm3": 118.0,
        "gas_supplier": {"name": "欣高石油氣股份有限公司", "ban": "76002807",
                         "unit_price_ntd_per_m3": 17.9},
        "electricity_mwh": 342.0,
        "plating_chemicals_ntd": 1_120_000,
        "machines": [
            {"name_zh": "冷鍛成型機", "name_en": "Cold former", "kw": 90, "hours": 3900, "process": "Carbon steel screws and nuts"},
            {"name_zh": "搓牙機", "name_en": "Thread roller", "kw": 30, "hours": 3900, "process": "Carbon steel screws and nuts"},
            {"name_zh": "網帶式熱處理爐", "name_en": "Mesh-belt furnace", "kw": 50, "hours": 5200, "process": "Carbon steel screws and nuts"},
        ],
    },
}

MONTH_SHAPE = [0.078, 0.070, 0.082, 0.080, 0.084, 0.090,
               0.096, 0.094, 0.090, 0.084, 0.078, 0.074]  # summer-weighted, sums to 1


# ---------------------------------------------------------------------------
# Renderers
# ---------------------------------------------------------------------------
def pdf_to_png(pdf_path: Path) -> None:
    import pypdfium2 as pdfium

    doc = pdfium.PdfDocument(str(pdf_path))
    page = doc[0]
    bitmap = page.render(scale=2.2)  # ~158 dpi, phone-photo-ish
    bitmap.to_pil().save(pdf_path.with_suffix(".png"))
    doc.close()


def draw_taipower_bill(path: Path, ident: dict, year: int, month: int,
                       kwh: dict, amounts: dict) -> None:
    """Stylized Taipower 高壓三段式 TOU bill — layout faithful enough for a parser test."""
    c = canvas.Canvas(str(path), pagesize=A4)
    w, h = A4

    c.setFont(ZH, 16)
    c.drawCentredString(w / 2, h - 18 * mm, "台灣電力股份有限公司")
    c.setFont(ZH, 12)
    c.drawCentredString(w / 2, h - 25 * mm, "電費通知單暨收據（高壓電力・三段式時間電價）")

    c.setFont(ZH, 9.5)
    y = h - 38 * mm
    rows1 = [
        ("用戶名稱", ident["name_zh"], "電號", ident["electricity_no"]),
        ("用電地址", ident["street"], "統一編號", ident["ban"]),
        ("計費年月", f"{year - 1911:03d}年{month:02d}月", "契約容量", f"{ident['contract_capacity_kw']} 瓩"),
        ("用電種類", "高壓電力三段式時間電價", "功率因數", "97%"),
    ]
    for a, b, cc, d in rows1:
        c.drawString(20 * mm, y, f"{a}：{b}")
        c.drawString(120 * mm, y, f"{cc}：{d}")
        y -= 6.5 * mm

    y -= 4 * mm
    c.setFont(ZH, 10.5)
    c.drawString(20 * mm, y, "本期用電度數")
    y -= 7 * mm
    c.setFont(ZH, 9.5)
    table = [
        ("時段", "度數 (kWh)", "單價 (元/度)", "金額 (元)"),
        ("尖峰", f"{kwh['peak']:,.0f}", f"{amounts['rate_peak']:.2f}", f"{kwh['peak'] * amounts['rate_peak']:,.0f}"),
        ("半尖峰", f"{kwh['half']:,.0f}", f"{amounts['rate_half']:.2f}", f"{kwh['half'] * amounts['rate_half']:,.0f}"),
        ("離峰", f"{kwh['off']:,.0f}", f"{amounts['rate_off']:.2f}", f"{kwh['off'] * amounts['rate_off']:,.0f}"),
        ("合計", f"{kwh['total']:,.0f}", "", ""),
    ]
    x_cols = [20, 60, 100, 140]
    for row in table:
        for x, cell in zip(x_cols, row):
            c.drawString(x * mm, y, str(cell))
        y -= 6.5 * mm
        if row is table[0]:
            c.line(20 * mm, y + 4.5 * mm, 180 * mm, y + 4.5 * mm)

    y -= 4 * mm
    for label, key in [("基本電費", "basic"), ("流動電費", "energy"),
                       ("功率因數折扣", "pf_discount"), ("本期電費總計", "total")]:
        c.setFont(ZH, 10.5 if key == "total" else 9.5)
        c.drawString(20 * mm, y, f"{label}：{amounts[key]:,.0f} 元")
        y -= 6.5 * mm

    c.setFont(ZH, 8)
    c.drawString(20 * mm, 22 * mm, "台電公司客服專線 1911 ・ 本單為模擬樣張（CarbonPass 測試語料，非真實帳單）")
    c.showPage()
    c.save()
    pdf_to_png(path)


def mig_f0401_xml(inv: dict) -> str:
    """Minimal-but-well-formed MIG 4.0 F0401 (B2B exchange) invoice XML."""
    details = []
    for i, it in enumerate(inv["items"], 1):
        details.append(f"""    <ProductItem>
      <Description>{escape(it['desc'])}</Description>
      <Quantity>{it['qty']}</Quantity>
      <Unit>{escape(it['unit'])}</Unit>
      <UnitPrice>{it['unit_price']}</UnitPrice>
      <Amount>{it['amount']}</Amount>
      <SequenceNumber>{i:03d}</SequenceNumber>
    </ProductItem>""")
    sales = inv["sales_amount"]
    tax = round(sales * 0.05)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<Invoice xmlns="urn:GEINV:eInvoiceMessage:F0401:4.0">
  <Main>
    <InvoiceNumber>{inv['number']}</InvoiceNumber>
    <InvoiceDate>{inv['date']}</InvoiceDate>
    <InvoiceTime>10:30:00</InvoiceTime>
    <Seller>
      <Identifier>{inv['seller_ban']}</Identifier>
      <Name>{escape(inv['seller_name'])}</Name>
    </Seller>
    <Buyer>
      <Identifier>{inv['buyer_ban']}</Identifier>
      <Name>{escape(inv['buyer_name'])}</Name>
    </Buyer>
    <InvoiceType>07</InvoiceType>
    <TaxType>1</TaxType>
  </Main>
  <Details>
{chr(10).join(details)}
  </Details>
  <Amount>
    <SalesAmount>{sales}</SalesAmount>
    <TaxAmount>{tax}</TaxAmount>
    <TotalAmount>{sales + tax}</TotalAmount>
  </Amount>
</Invoice>
"""


def draw_invoice_pdf(path: Path, inv: dict) -> None:
    """電子發票證明聯-style render of the same invoice for the VLM path."""
    c = canvas.Canvas(str(path), pagesize=A4)
    w, h = A4
    c.setFont(ZH, 14)
    c.drawCentredString(w / 2, h - 18 * mm, f"{inv['seller_name']}")
    c.setFont(ZH, 12)
    c.drawCentredString(w / 2, h - 26 * mm, "電子發票證明聯")
    c.setFont(ZH, 10)
    y2 = int(inv["date"][:4]) - 1911
    mm_ = int(inv["date"][4:6])
    period = f"{y2:03d}年{mm_ - (1 - mm_ % 2):02d}-{mm_ + (mm_ % 2 == 0) * 0 + (1 - mm_ % 2):02d}月" \
        if False else f"{y2:03d}年{mm_:02d}月"
    c.drawCentredString(w / 2, h - 33 * mm, f"{period}  {inv['number'][:2]}-{inv['number'][2:]}")
    c.setFont(ZH, 9.5)
    y = h - 45 * mm
    c.drawString(20 * mm, y, f"賣方統編：{inv['seller_ban']}    買方統編：{inv['buyer_ban']}")
    y -= 6 * mm
    c.drawString(20 * mm, y, f"買受人：{inv['buyer_name']}")
    y -= 6 * mm
    c.drawString(20 * mm, y, f"發票日期：{inv['date'][:4]}/{inv['date'][4:6]}/{inv['date'][6:]}")
    y -= 9 * mm
    c.drawString(20 * mm, y, "品名")
    c.drawString(95 * mm, y, "數量")
    c.drawString(120 * mm, y, "單位")
    c.drawString(140 * mm, y, "單價")
    c.drawString(165 * mm, y, "金額")
    y -= 2 * mm
    c.line(20 * mm, y, 190 * mm, y)
    y -= 6 * mm
    for it in inv["items"]:
        c.drawString(20 * mm, y, it["desc"][:34])
        c.drawRightString(112 * mm, y, f"{it['qty']:,}")
        c.drawString(120 * mm, y, it["unit"])
        c.drawRightString(158 * mm, y, f"{it['unit_price']:,.2f}")
        c.drawRightString(190 * mm, y, f"{it['amount']:,}")
        y -= 6.5 * mm
    y -= 3 * mm
    sales = inv["sales_amount"]
    tax = round(sales * 0.05)
    c.drawRightString(190 * mm, y, f"銷售額合計：{sales:,}")
    y -= 6 * mm
    c.drawRightString(190 * mm, y, f"營業稅：{tax:,}")
    y -= 6 * mm
    c.setFont(ZH, 10.5)
    c.drawRightString(190 * mm, y, f"總計：{sales + tax:,}")
    c.setFont(ZH, 8)
    c.drawString(20 * mm, 22 * mm, "本張為模擬樣張（CarbonPass 測試語料，非真實發票）")
    c.showPage()
    c.save()
    pdf_to_png(path)


def draw_production_log(path: Path, firm: dict, monthly: dict) -> None:
    c = canvas.Canvas(str(path), pagesize=A4)
    w, h = A4
    c.setFont(ZH, 14)
    c.drawCentredString(w / 2, h - 18 * mm, f"{firm['identity']['name_zh']}  {PERIOD_YEAR} 年度生產日誌彙總")
    c.setFont(ZH, 9)
    y = h - 30 * mm
    c.drawString(15 * mm, y, "月份")
    x = 45 * mm
    for p in firm["processes"]:
        c.drawString(x, y, f"{p['name'][:22]} (CN {p['cn_code']}) 噸")
        x += 62 * mm
    y -= 2 * mm
    c.line(15 * mm, y, 195 * mm, y)
    y -= 6 * mm
    for m in range(1, 13):
        c.drawString(15 * mm, y, f"{m:02d}")
        x = 45 * mm
        for p in firm["processes"]:
            c.drawRightString(x + 30 * mm, y, f"{monthly[p['name']][m - 1]:.1f}")
            x += 62 * mm
        y -= 6 * mm
    c.drawString(15 * mm, y, "合計")
    x = 45 * mm
    for p in firm["processes"]:
        c.drawRightString(x + 30 * mm, y, f"{sum(monthly[p['name']]):.1f}")
        x += 62 * mm

    y -= 12 * mm
    c.setFont(ZH, 11)
    c.drawString(15 * mm, y, "主要機台清單")
    y -= 7 * mm
    c.setFont(ZH, 9)
    c.drawString(15 * mm, y, "機台")
    c.drawString(70 * mm, y, "額定功率 (kW)")
    c.drawString(110 * mm, y, "年運轉時數 (h)")
    c.drawString(150 * mm, y, "所屬產線")
    y -= 2 * mm
    c.line(15 * mm, y, 195 * mm, y)
    y -= 6 * mm
    for mach in firm["machines"]:
        c.drawString(15 * mm, y, f"{mach['name_zh']} / {mach['name_en']}"[:38])
        c.drawRightString(95 * mm, y, str(mach["kw"]))
        c.drawRightString(135 * mm, y, str(mach["hours"]))
        c.drawString(150 * mm, y, "共用" if mach["process"] == "shared" else mach["process"][:18])
        y -= 6 * mm
    c.setFont(ZH, 8)
    c.drawString(15 * mm, 18 * mm, "模擬樣張（CarbonPass 測試語料）")
    c.showPage()
    c.save()
    pdf_to_png(path)


# ---------------------------------------------------------------------------
# Ground-truth SEE (hand math, mirrors the answer-key chain)
# ---------------------------------------------------------------------------
def compute_ground_truth(firm: dict) -> dict:
    gas_tj = firm["natural_gas_knm3"] * NG_NCV_GJ_PER_KNM3 / 1000.0
    gas_co2 = gas_tj * NG_EF_TCO2_PER_TJ
    total_prod = sum(p["production_t"] for p in firm["processes"])

    # Step 1: attribute installation-level fuel + electricity to processes.
    # Gas: by production tonnes (heat demand ~ throughput). Electricity: by
    # machine kW x hours (shared machines split by production tonnes).
    elec_share = {p["name"]: 0.0 for p in firm["processes"]}
    kwh_weights = {p["name"]: 0.0 for p in firm["processes"]}
    for mach in firm["machines"]:
        e = mach["kw"] * mach["hours"]
        if mach["process"] == "shared":
            for p in firm["processes"]:
                kwh_weights[p["name"]] += e * p["production_t"] / total_prod
        else:
            kwh_weights[mach["process"]] += e
    wsum = sum(kwh_weights.values())
    for k in kwh_weights:
        elec_share[k] = kwh_weights[k] / wsum

    products = []
    for p in firm["processes"]:
        al = p["production_t"]
        dir_em = gas_co2 * (al / total_prod)          # gas split by tonnes
        elec_mwh = firm["electricity_mwh"] * elec_share[p["name"]]
        se_dir_own = dir_em / al
        se_ind_own = elec_mwh * GRID_EF / al          # tCO2e/t (EF kg/kWh == t/MWh)

        see_dir, see_ind, embedded_elec, default_share_num = se_dir_own, se_ind_own, elec_mwh / al, 0.0
        precursor_lines = []
        for prec in firm["precursors"]:
            m = prec["consumed_t"].get(p["name"], 0.0)
            if m == 0.0:
                continue
            ratio = m / al
            if prec["epd"]:
                psd = prec["epd"]["see_direct"]
                pse = prec["epd"]["spec_electricity_mwh_per_t"]
                psi = pse * prec["epd"]["electricity_ef"]
                source = "actual"
            else:
                psd = (DEFAULT_SEE_WIRE_ROD_7213_2026
                       if prec["cn_code_precursor"] == "7213"
                       else DEFAULT_SEE_WIRE_ROD_7221_2026)
                pse, psi = 0.0, 0.0   # defaults carry no indirect for steel (N/A)
                source = "default"
                default_share_num += ratio * psd
            see_dir += ratio * psd
            see_ind += ratio * psi
            embedded_elec += ratio * pse
            precursor_lines.append({
                "precursor": prec["name"], "consumed_t": m, "ratio_t_per_t": ratio,
                "see_direct_used": psd, "see_indirect_used": psi, "source": source,
            })

        products.append({
            "product_name": p["name"],
            "cn_code": p["cn_code"],
            "production_t": al,
            "direct_attributed_emissions_tco2e": round(dir_em, 6),
            "electricity_mwh": round(elec_mwh, 6),
            "se_direct_own": round(se_dir_own, 9),
            "se_indirect_own": round(se_ind_own, 9),
            "precursors": precursor_lines,
            "see_direct": round(see_dir, 9),
            "see_indirect": round(see_ind, 9),
            "see_total": round(see_dir + see_ind, 9),
            "embedded_electricity_mwh_per_t": round(embedded_elec, 9),
            "share_default_values": round(default_share_num / see_dir, 6) if see_dir else 0.0,
        })

    return {
        "period": {"start": f"{PERIOD_YEAR}-01-01", "end": f"{PERIOD_YEAR}-12-31"},
        "installation_totals": {
            "natural_gas_knm3": firm["natural_gas_knm3"],
            "fuel_input_tj": round(gas_tj, 6),
            "total_direct_emissions_tco2e": round(gas_co2, 6),
            "electricity_mwh": firm["electricity_mwh"],
            "total_indirect_emissions_tco2e": round(firm["electricity_mwh"] * GRID_EF, 6),
        },
        "products": products,
    }


# ---------------------------------------------------------------------------
# Document generation per firm
# ---------------------------------------------------------------------------
def monthly_split(total: float, rng: random.Random, jitter: float = 0.06) -> list[float]:
    raw = [s * (1 + rng.uniform(-jitter, jitter)) for s in MONTH_SHAPE]
    k = total / sum(raw)
    return [r * k for r in raw]


def make_firm(firm_key: str, firm: dict) -> dict:
    rng = random.Random(firm["seed"])
    fdir = OUT / firm_key
    (fdir / "bills").mkdir(parents=True, exist_ok=True)
    (fdir / "invoices").mkdir(parents=True, exist_ok=True)

    ident = firm["identity"]
    # firm.json = owner-onboarding data (the LINE Q&A stand-in): identity, the
    # process map defined at first-time setup (docs/archive/10 §2A), machine priors, and
    # any mill EPD the owner uploaded. Everything else comes from documents.
    onboarding = {
        "identity": ident,
        "period_year": PERIOD_YEAR,
        "processes": [{"name": p["name"], "cn_code": p["cn_code"],
                       "invoice_name": p["invoice_name"]} for p in firm["processes"]],
        "machines": firm["machines"],
        "precursor_epds": {
            prec["name"]: prec["epd"] for prec in firm["precursors"] if prec["epd"]
        },
        "precursor_consumption_t": {
            prec["name"]: {"consumed_t": prec["consumed_t"],
                           "consumed_other_t": prec["consumed_other_t"]}
            for prec in firm["precursors"]
        },
    }
    (fdir / "firm.json").write_text(
        json.dumps(onboarding, ensure_ascii=False, indent=2), encoding="utf-8")

    # --- Taipower bills ------------------------------------------------------
    kwh_months = monthly_split(firm["electricity_mwh"] * 1000, rng)
    bills_expected = []
    for m in range(1, 13):
        season = "summer" if 6 <= m <= 9 else "nonsummer"
        r = RATES[season]
        tot = kwh_months[m - 1]
        peak = tot * rng.uniform(0.16, 0.20)
        half = tot * rng.uniform(0.30, 0.36)
        off = tot - peak - half
        kwh = {"peak": round(peak), "half": round(half), "off": round(off)}
        kwh["total"] = kwh["peak"] + kwh["half"] + kwh["off"]
        basic = ident["contract_capacity_kw"] * RATES["capacity_ntd_per_kw"]
        energy = kwh["peak"] * r["peak"] + kwh["half"] * r["half"] + kwh["off"] * r["off"]
        amounts = {
            "rate_peak": r["peak"], "rate_half": r["half"], "rate_off": r["off"],
            "basic": round(basic), "energy": round(energy),
            "pf_discount": -round((basic + energy) * 0.015),
        }
        amounts["total"] = amounts["basic"] + amounts["energy"] + amounts["pf_discount"]
        path = fdir / "bills" / f"taipower_{PERIOD_YEAR}_{m:02d}.pdf"
        draw_taipower_bill(path, ident, PERIOD_YEAR, m, kwh, amounts)
        bills_expected.append({
            "file": str(path.relative_to(OUT)), "year": PERIOD_YEAR, "month": m,
            "kwh_peak": kwh["peak"], "kwh_half_peak": kwh["half"], "kwh_off_peak": kwh["off"],
            "kwh_total": kwh["total"], "total_ntd": amounts["total"],
            "contract_capacity_kw": ident["contract_capacity_kw"],
            "electricity_no": ident["electricity_no"],
        })

    # --- e-invoices (steel quarterly, gas monthly, chemicals bi-monthly) -----
    invoices_expected = []
    inv_seq = 0

    def emit_invoice(date_: date, seller: str, seller_ban: str, items: list[dict], tag: str):
        nonlocal inv_seq
        inv_seq += 1
        number = f"{'ABCDEFGHJK'[firm['seed'] % 10]}{'BCDEFGHJKA'[inv_seq % 10]}{10000000 + firm['seed'] * 97 + inv_seq * 13:08d}"
        inv = {
            "number": number,
            "date": date_.strftime("%Y%m%d"),
            "seller_name": seller, "seller_ban": seller_ban,
            "buyer_name": ident["name_zh"], "buyer_ban": ident["ban"],
            "items": items,
            "sales_amount": sum(i["amount"] for i in items),
        }
        stem = f"{tag}_{date_.strftime('%Y%m%d')}_{number}"
        (fdir / "invoices" / f"{stem}.xml").write_text(mig_f0401_xml(inv), encoding="utf-8")
        draw_invoice_pdf(fdir / "invoices" / f"{stem}.pdf", inv)
        invoices_expected.append({
            "file": str((fdir / "invoices" / f"{stem}.xml").relative_to(OUT)),
            "number": number, "date": inv["date"], "seller_ban": seller_ban,
            "category": tag, "items": items,
        })

    for prec in firm["precursors"]:
        q_t = prec["purchased_t"] / 4.0
        for q, month in enumerate((2, 5, 8, 11)):
            kg = round(q_t * 1000)
            price = prec["unit_price_ntd_per_kg"]
            emit_invoice(
                date(PERIOD_YEAR, month, 8 + q), prec["supplier"], prec["supplier_ban"],
                [{"desc": f"{prec['grade']} 盤元線材 {prec['name']}",
                  "qty": kg, "unit": "公斤", "unit_price": price, "amount": round(kg * price)}],
                tag=f"steel_{prec['grade']}",
            )

    gas_months = monthly_split(firm["natural_gas_knm3"] * 1000, rng)  # m3
    gas_m3_emitted = 0
    for m in range(1, 13):
        m3 = round(gas_months[m - 1])
        gas_m3_emitted += m3
        price = firm["gas_supplier"]["unit_price_ntd_per_m3"]
        emit_invoice(
            date(PERIOD_YEAR, m, 20), firm["gas_supplier"]["name"], firm["gas_supplier"]["ban"],
            [{"desc": "天然氣（工業用）", "qty": m3, "unit": "立方公尺",
              "unit_price": price, "amount": round(m3 * price)}],
            tag="gas",
        )

    for i, m in enumerate((1, 3, 5, 7, 9, 11)):
        amt = round(firm["plating_chemicals_ntd"] / 6)
        emit_invoice(
            date(PERIOD_YEAR, m, 12), "台灣表面處理化學股份有限公司", "28445566",
            [{"desc": "電鍍藥劑（鋅酸鹽系）", "qty": 1, "unit": "批",
              "unit_price": amt, "amount": amt}],
            tag="chemicals",
        )

    # --- production log ------------------------------------------------------
    monthly_prod = {p["name"]: monthly_split(p["production_t"], rng) for p in firm["processes"]}
    rows = []
    for m in range(1, 13):
        row = {"month": m}
        for p in firm["processes"]:
            row[p["cn_code"]] = round(monthly_prod[p["name"]][m - 1], 1)
        rows.append(row)
    csv_lines = ["month," + ",".join(f"cn_{p['cn_code']}_t" for p in firm["processes"])]
    for row in rows:
        csv_lines.append(str(row["month"]) + "," + ",".join(str(row[p["cn_code"]]) for p in firm["processes"]))
    (fdir / "production_log.csv").write_text("\n".join(csv_lines) + "\n", encoding="utf-8")
    draw_production_log(fdir / "production_log.pdf", firm, monthly_prod)

    # Ground truth from the rows the documents ACTUALLY carry, not the intended
    # totals (docs/archive/15 §6 defect 11): monthly production rounds to 0.1 t, gas m3 and
    # bill kWh round to integers — the engine can only ever see the rounded sums,
    # so the golden must be computed from them.
    emitted = {
        **firm,
        "processes": [
            {**p, "production_t": round(sum(r[p["cn_code"]] for r in rows), 6)}
            for p in firm["processes"]
        ],
        "natural_gas_knm3": gas_m3_emitted / 1000.0,
        "electricity_mwh": sum(b["kwh_total"] for b in bills_expected) / 1000.0,
    }
    gt = compute_ground_truth(emitted)
    gt["expected_extractions"] = {
        "bills": bills_expected,
        "invoices": invoices_expected,
        "production_log": {"file": str((fdir / "production_log.csv").relative_to(OUT)), "rows": rows},
        "machines": firm["machines"],
    }
    gt["identity"] = ident
    return gt


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    truth = {"_generated_by": "scripts/make_mock_corpus.py", "period_year": PERIOD_YEAR,
             "grid_ef_kgco2_per_kwh": GRID_EF, "firms": {}}
    for key, firm in FIRMS.items():
        print(f"generating {key} ...")
        truth["firms"][key] = make_firm(key, firm)
    (OUT / "ground_truth.json").write_text(
        json.dumps(truth, ensure_ascii=False, indent=2), encoding="utf-8")
    n_files = sum(1 for _ in OUT.rglob("*") if _.is_file())
    print(f"OK: corpus at {OUT} ({n_files} files)")
    for key, g in truth["firms"].items():
        for p in g["products"]:
            print(f"  {key}: CN {p['cn_code']}  SEE dir {p['see_direct']:.4f}  "
                  f"ind {p['see_indirect']:.4f}  total {p['see_total']:.4f} tCO2e/t "
                  f"(default share {p['share_default_values']:.0%})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
