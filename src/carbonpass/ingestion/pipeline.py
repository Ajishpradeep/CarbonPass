"""Ingestion pipeline: a firm's document folder -> validated activity_data JSON.

Order of preference per docs/10 §2A:
  1. structured e-invoice XML (MIG 4.0) for steel & fuel purchases   [egui.parser]
  2. VLM photo/PDF parse for the Taipower bill (no open schema)      [vlm + docling]
  3. CSV/owner-confirmed data for production log & machine priors

Every aggregated quantity carries {value, source, confidence, uncertainty_rel,
document_refs}. The pipeline validates the result against
schema/activity_data.schema.json before writing.
"""
from __future__ import annotations

import json
import statistics
from pathlib import Path

import jsonschema

from carbonpass.config import ACTIVITY_SCHEMA_JSON
from carbonpass.egui.parser import categorize_item, classify_validate, parse_mig_invoice

# NCV/EF defaults for fuels named on Taiwanese invoices (template example values;
# MOENV coefficient DB provides alternatives via carbonpass.rules.ef).
FUEL_CONSTANTS = {
    "natural_gas": {"unit": "1000 Nm3", "ncv_gj_per_unit": 38.5, "ef_tco2_per_tj": 56.1,
                    "ef_source": "IPCC 2006 / template example"},
}

# VLM-derived quantities: relative uncertainty grows as confidence drops.
def _vlm_uncertainty(confidence: float) -> float:
    return round(0.005 + (1.0 - confidence) * 0.10, 6)


STAINLESS_PAT = ("SUS", "不鏽", "不銹", "stainless")


def _is_stainless(grade_or_desc: str) -> bool:
    return any(p.lower() in grade_or_desc.lower() for p in STAINLESS_PAT)


def _precursor_cn(grade_or_desc: str) -> str:
    """CN code of the wire rod (盤元線材) a fastener plant buys and draws itself.

    Both codes are the same product in different grades — "hot-rolled, in irregularly
    wound coils":
        CN 7213  iron / non-alloy steel   (Taiwan 2.298)
        CN 7221  stainless steel          (Taiwan: NO VALUE -> Annex I fallback 4.82)

    Do NOT use CN 7227 here: that is "bars and rods of alloy steel **other than
    stainless**", and Taiwan's 7227 (2.17) is the lowest value assigned to any country on
    earth — using it for stainless understated the precursor ~2.2x and silently made a
    stainless screw look cleaner than a carbon one. Nor CN 7222/7223, which are other
    bars/rods and *drawn wire* — a fastener plant buys rod and draws it in-house (see the
    抽線機 in every firm's machine list).
    """
    return "7221" if _is_stainless(grade_or_desc) else "7213"


def ingest_firm(firm_dir: str | Path, use_vlm: bool = True) -> dict:
    firm_dir = Path(firm_dir)
    onboarding = json.loads((firm_dir / "firm.json").read_text(encoding="utf-8"))
    ident = onboarding["identity"]
    year = onboarding["period_year"]

    documents: list[dict] = []

    # ---- 1. e-invoices (structured XML) -------------------------------------
    steel_by_key: dict[str, dict] = {}
    gas_m3, gas_refs = 0.0, []
    for xml_path in sorted((firm_dir / "invoices").glob("*.xml")):
        inv = parse_mig_invoice(xml_path)
        validation = classify_validate(inv)
        documents.append({
            "type": "egui_invoice",
            "file": str(xml_path.relative_to(firm_dir)),
            "parser": "mig_xml",
            "fields": inv,
            "confidence": {"all": 1.0},   # signed structured XML
            "validation": validation,
        })
        for item in inv["items"]:
            cat = categorize_item(item)
            if cat == "steel" and item["quantity"]:
                kg = item["quantity"] if item["unit"] in ("公斤", "kg", "KG") else item["quantity"] * 1000.0
                key = item["description"]
                rec = steel_by_key.setdefault(key, {
                    "description": key, "mass_kg": 0.0,
                    "supplier": inv["seller_name"], "supplier_ban": inv["seller_ban"],
                    "refs": [],
                })
                rec["mass_kg"] += kg
                rec["refs"].append(str(xml_path.name))
            elif cat == "gas" and item["quantity"]:
                gas_m3 += item["quantity"]
                gas_refs.append(str(xml_path.name))

    # ---- 2. Taipower bills (VLM path) ---------------------------------------
    kwh_by_month: dict[int, float] = {}
    bill_confidences: list[float] = []
    bill_refs: list[str] = []
    bills = sorted((firm_dir / "bills").glob("*.png"))
    if use_vlm and bills:
        from carbonpass.ingestion.docling_pass import layout_text
        from carbonpass.ingestion.vlm import extract_from_image, ollama_available

        if not ollama_available():
            raise RuntimeError(
                "Ollama is not reachable and --no-vlm was not given. "
                "Start `ollama serve` + pull the model, or rerun with --no-vlm.")
        from carbonpass.ingestion.backstop import apply_to_document

        for k, png in enumerate(bills, 1):
            print(f"[ingest] bill {k}/{len(bills)}: {png.name}", flush=True)
            pdf = png.with_suffix(".pdf")
            context = layout_text(pdf if pdf.exists() else png)
            fields = extract_from_image(png, "taipower_bill", context_text=context)
            conf = fields.pop("confidence", {}) or {}
            checks, ok = [], True
            parts = [fields.get("kwh_peak"), fields.get("kwh_half_peak"), fields.get("kwh_off_peak")]
            if all(isinstance(x, (int, float)) for x in parts) and isinstance(fields.get("kwh_total"), (int, float)):
                s = sum(parts)
                good = abs(s - fields["kwh_total"]) <= max(2.0, 0.005 * fields["kwh_total"])
                checks.append(f"peak+half+off={s} vs total={fields['kwh_total']}: {'OK' if good else 'MISMATCH'}")
                ok &= good
            doc = {
                "type": "taipower_bill",
                "file": str(png.relative_to(firm_dir)),
                "parser": "vlm",
                "fields": fields,
                "confidence": {k: float(v) for k, v in conf.items() if isinstance(v, (int, float))},
                "validation": {"passed": bool(ok), "checks": checks},
            }
            # numeric backstop: independent PP-OCRv4 text vs the VLM's numbers
            apply_to_document(doc, context)
            documents.append(doc)
            if isinstance(fields.get("billing_month"), (int, float)) and isinstance(fields.get("kwh_total"), (int, float)):
                kwh_by_month[int(fields["billing_month"])] = float(fields["kwh_total"])
            numeric_confs = [v for v in conf.values() if isinstance(v, (int, float))]
            if numeric_confs:
                bill_confidences.append(statistics.fmean(numeric_confs))
            bill_refs.append(str(png.name))
    elif bills:
        print("[ingest] --no-vlm: skipping Taipower bill parse (electricity from bills unavailable)")

    # ---- 3. production log (CSV, owner-confirmed) ---------------------------
    prod_by_cn: dict[str, float] = {}
    csv_path = firm_dir / "production_log.csv"
    if csv_path.exists():
        lines = csv_path.read_text(encoding="utf-8").strip().splitlines()
        header = lines[0].split(",")
        cn_cols = [(i, h.removeprefix("cn_").removesuffix("_t")) for i, h in enumerate(header) if h.startswith("cn_")]
        for line in lines[1:]:
            vals = line.split(",")
            for i, cn in cn_cols:
                prod_by_cn[cn] = prod_by_cn.get(cn, 0.0) + float(vals[i])
        documents.append({
            "type": "production_log",
            "file": "production_log.csv",
            "parser": "csv",
            "fields": {"totals_by_cn": {k: round(v, 3) for k, v in prod_by_cn.items()}},
            "confidence": {"all": 1.0},
            "validation": {"passed": True, "checks": []},
        })

    # ---- aggregate -----------------------------------------------------------
    mean_bill_conf = statistics.fmean(bill_confidences) if bill_confidences else 0.0
    electricity_mwh = round(sum(kwh_by_month.values()) / 1000.0, 6)
    aggregated: dict = {
        "electricity_mwh": {
            "value": electricity_mwh,
            "unit": "MWh",
            "source": "actual",
            "confidence": round(mean_bill_conf, 4),
            "uncertainty_rel": _vlm_uncertainty(mean_bill_conf) if bill_confidences else 0.0,
            "n_documents": len(kwh_by_month),
            "document_refs": bill_refs,
        },
        "electricity_kwh_by_month": [kwh_by_month.get(m, 0.0) for m in range(1, 13)],
        "fuels": [],
        "steel_inputs": [],
        "production": [],
        "machines": [
            {"name": m.get("name") or m.get("name_en") or m.get("name_zh", "machine"),
             "kw": m["kw"], "hours": m["hours"], "process": m.get("process", "shared")}
            for m in onboarding.get("machines", [])
        ],
    }
    if gas_m3 > 0:
        c = FUEL_CONSTANTS["natural_gas"]
        aggregated["fuels"].append({
            "name": "Natural gas",
            "method": "Combustion",
            "amount": {"value": round(gas_m3 / 1000.0, 6), "unit": "1000 Nm3", "source": "actual",
                       "confidence": 1.0, "uncertainty_rel": 0.005,
                       "n_documents": len(gas_refs), "document_refs": gas_refs},
            "unit": c["unit"], "ncv_gj_per_unit": c["ncv_gj_per_unit"],
            "ef_tco2_per_tj": c["ef_tco2_per_tj"], "ef_source": c["ef_source"],
        })
    epds = onboarding.get("precursor_epds", {})
    consumption = onboarding.get("precursor_consumption_t", {})
    for rec in steel_by_key.values():
        cn = _precursor_cn(rec["description"])
        name = ("Stainless steel wire rod" if _is_stainless(rec["description"])
                else "Carbon steel wire rod")
        aggregated["steel_inputs"].append({
            "name": name,
            "grade": rec["description"],
            "cn_code_precursor": cn,
            "country": "TW",
            "supplier": rec["supplier"],
            "supplier_ban": rec["supplier_ban"],
            "mass_t": {"value": round(rec["mass_kg"] / 1000.0, 6), "unit": "t", "source": "actual",
                       "confidence": 1.0, "uncertainty_rel": 0.005,
                       "n_documents": len(rec["refs"]), "document_refs": rec["refs"]},
            "epd": epds.get(name),
            "consumption_t": consumption.get(name),
        })
    proc_by_cn = {p["cn_code"]: p for p in onboarding.get("processes", [])}
    for cn, tonnes in sorted(prod_by_cn.items()):
        p = proc_by_cn.get(cn, {})
        aggregated["production"].append({
            "process_name": p.get("name", f"CN {cn}"),
            "cn_code": cn,
            "invoice_name": p.get("invoice_name", ""),
            "tonnes": {"value": round(tonnes, 3), "unit": "t", "source": "actual",
                       "confidence": 1.0, "uncertainty_rel": 0.01,
                       "n_documents": 1, "document_refs": ["production_log.csv"]},
        })

    activity = {
        "installation": {
            "name_zh": ident.get("name_zh"), "name_en": ident["name_en"],
            "ban": ident.get("ban"), "street": ident.get("street"),
            "city": ident.get("city"), "post_code": ident.get("post_code"),
            "country": ident["country"], "unlocode": ident.get("unlocode"),
            "latitude": ident.get("latitude"), "longitude": ident.get("longitude"),
            "economic_activity": ident.get("economic_activity"),
            "electricity_no": ident.get("electricity_no"),
            "contract_capacity_kw": ident.get("contract_capacity_kw"),
        },
        "period": {"start": f"{year}-01-01", "end": f"{year}-12-31", "year": year},
        "documents": documents,
        "aggregated": aggregated,
    }

    schema = json.loads(ACTIVITY_SCHEMA_JSON.read_text(encoding="utf-8"))
    jsonschema.validate(activity, schema)
    return activity


def accuracy_report(activity: dict, ground_truth_path: Path, firm_key: str) -> dict | None:
    """Field-level accuracy of VLM bill extraction vs corpus ground truth."""
    if not ground_truth_path.exists():
        return None
    gt = json.loads(ground_truth_path.read_text(encoding="utf-8"))["firms"].get(firm_key)
    if gt is None:
        return None
    from carbonpass.ingestion.scoring import BILL_FIELDS, score_fields

    expected_bills = {b["month"]: b for b in gt["expected_extractions"]["bills"]}
    n_ok = n_tot = 0
    per_field = {f: {"ok": 0, "tot": 0} for f in BILL_FIELDS}
    for doc in activity["documents"]:
        if doc["type"] != "taipower_bill":
            continue
        m = doc["fields"].get("billing_month")
        exp = expected_bills.get(int(m)) if isinstance(m, (int, float)) else None
        if exp is None:
            continue
        for f, ok in score_fields(doc["fields"], exp, BILL_FIELDS).items():
            per_field[f]["tot"] += 1
            n_tot += 1
            if ok:
                per_field[f]["ok"] += 1
                n_ok += 1
    elec = activity["aggregated"]["electricity_mwh"]["value"]
    elec_want = gt["installation_totals"]["electricity_mwh"]
    return {
        "bill_fields_correct": n_ok, "bill_fields_total": n_tot,
        "bill_field_accuracy": round(n_ok / n_tot, 4) if n_tot else None,
        "per_field": {f: v for f, v in per_field.items() if v["tot"]},
        "electricity_mwh": {"extracted": elec, "expected": elec_want,
                            "rel_error": round(abs(elec - elec_want) / elec_want, 6) if elec_want else None},
    }


def run_ingest_cli(firm_dir: str, output: str | None, use_vlm: bool = True) -> int:
    firm_path = Path(firm_dir)
    activity = ingest_firm(firm_path, use_vlm=use_vlm)
    out = Path(output) if output else Path("out") / f"{firm_path.name}_activity.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(activity, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK: activity data -> {out} (schema-valid, {len(activity['documents'])} documents)")

    report = accuracy_report(activity, firm_path.parent / "ground_truth.json", firm_path.name)
    if report:
        print("Extraction accuracy vs ground truth:")
        print(json.dumps(report, indent=2))
    return 0
