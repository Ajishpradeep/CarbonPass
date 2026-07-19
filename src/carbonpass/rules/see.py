"""SEE engine — Specific Embedded Emissions per IR 2025/2547 (complex goods).

    SEE_dir(good) = DirEm(p)/AL(p) + Σ_i m_i/AL(p) · SEE_dir(prec_i)
    SEE_ind(good) = Elec(p)·EF/AL(p) + Σ_i m_i/AL(p) · SEE_ind(prec_i)
    EmbElec(good) = Elec(p)/AL(p)   + Σ_i m_i/AL(p) · SpecElec(prec_i)

Computed ONCE per determination period (calendar year) per CN good — never
per shipment. Verified against the Commission's screws & nuts answer key
(tests/golden). Precursor SEE comes from a mill EPD when supplied (source
'actual'), else from the CBAM default value for the precursor CN code with the
period's mark-up derived from the workbook row itself (steel 10/20/30%,
fertilisers flat 1% — source 'default'). Defaults are lawful without limit
(IR 2025/2547 Annex II A.1.2, docs/15 §8.1); their share is recorded, not capped.

Indirect SEE is computed and recorded (the template requires it) but is NOT
part of the CN 7318 certificate obligation (G7) — cost math must use direct only.

Every line carries {value, source, uncertainty_rel}. This module PREPARES
verification; it never certifies.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

from carbonpass.config import indirect_in_certificate
from carbonpass.rules import defaults


@dataclass
class Line:
    """One emitted figure with provenance — the unit of verifier-readiness."""
    value: float
    source: str                    # actual | default | estimate
    uncertainty_rel: float = 0.0   # relative 1-sigma
    note: str = ""


@dataclass
class PrecursorInput:
    name: str
    mass_t: float                  # consumed in this process over the period
    mass_unc_rel: float = 0.005
    cn_code: str = ""              # precursor CN (for default lookup)
    country: str = "Taiwan"        # sheet in default_values.xlsx
    # actual data (mill EPD) — if see_direct is None, defaults are used
    see_direct: float | None = None
    spec_electricity_mwh_per_t: float = 0.0
    electricity_ef: float = 0.0
    epd_document: str = ""


@dataclass
class ProcessInput:
    name: str
    cn_code: str
    production_t: float
    production_unc_rel: float
    direct_emissions_tco2e: float      # from the allocation engine
    direct_unc_rel: float
    electricity_mwh: float
    electricity_unc_rel: float
    electricity_ef: float              # tCO2/MWh (from rules/gridef.py — dated config)
    electricity_ef_source: str = "D.4.1"
    precursors: list[PrecursorInput] = field(default_factory=list)
    invoice_name: str = ""


@dataclass
class ProductSEE:
    product_name: str
    cn_code: str
    invoice_name: str
    see_direct: Line
    see_indirect: Line
    see_total: Line
    embedded_electricity_mwh_per_t: Line
    share_default_values: float
    precursor_lines: list[dict]
    needs_attention: list[str]


def _combine_rel(*terms: tuple[float, float]) -> float:
    """1-sigma of a sum of independent terms given (value, rel_unc) pairs."""
    total = sum(v for v, _ in terms)
    if total == 0:
        return 0.0
    var = sum((v * r) ** 2 for v, r in terms)
    return math.sqrt(var) / abs(total)


def compute_product_see(p: ProcessInput, period_year: int) -> ProductSEE:
    al = p.production_t
    needs_attention: list[str] = []

    # own process
    se_dir_own = p.direct_emissions_tco2e / al
    se_ind_own = p.electricity_mwh * p.electricity_ef / al
    elec_own = p.electricity_mwh / al
    own_unc = math.hypot(p.direct_unc_rel, p.production_unc_rel)

    dir_terms: list[tuple[float, float]] = [(se_dir_own, own_unc)]
    ind_terms: list[tuple[float, float]] = [
        (se_ind_own, math.hypot(p.electricity_unc_rel, p.production_unc_rel))]
    elec_terms: list[tuple[float, float]] = [
        (elec_own, math.hypot(p.electricity_unc_rel, p.production_unc_rel))]

    prec_lines, default_dir_sum = [], 0.0
    any_actual_prec = False
    for prec in p.precursors:
        ratio = prec.mass_t / al
        ratio_unc = math.hypot(prec.mass_unc_rel, p.production_unc_rel)
        if prec.see_direct is not None:
            psd = prec.see_direct
            psi = prec.spec_electricity_mwh_per_t * prec.electricity_ef
            pse = prec.spec_electricity_mwh_per_t
            source, psd_unc = "actual", 0.05     # EPD figure, third-party verified
            note = f"mill EPD: {prec.epd_document}" if prec.epd_document else "mill EPD"
            any_actual_prec = True
        else:
            dv, used_fallback = (defaults.resolve(prec.cn_code, prec.country)
                                 if prec.cn_code else (None, False))
            if dv is None or dv.for_year_direct(period_year) is None:
                raise ValueError(
                    f"precursor {prec.name!r}: no EPD and no default value for "
                    f"CN {prec.cn_code!r} ({prec.country}), and none in the "
                    f"'Other countries and territories' table either")
            # Mark-up basis: the workbook's marked-up column is TOTAL-based; split
            # direct/indirect with the row-derived mark-up (docs/15 §6 defects 1–2).
            psd = dv.for_year_direct(period_year)
            psi = dv.for_year_indirect(period_year) or 0.0
            pse = 0.0                  # defaults carry no specific-electricity figure
            markup = dv.derived_markup(period_year)
            source, psd_unc = "default", 0.0     # a default is exact — just punitive
            origin = (f"'Other countries and territories' — {prec.country} has no CN "
                      f"{prec.cn_code} row (IR 2025/2621 Annex I preamble; Q&A p.37)"
                      if used_fallback else prec.country)
            note = (f"CBAM default CN {dv.cn_code} ({origin}) direct {dv.direct} "
                    f"+{markup:.1%} row mark-up = {psd:.6g}"
                    + (f"; indirect {dv.indirect} -> {psi:.6g}" if psi else ""))
            default_dir_sum += ratio * psd
            needs_attention.append(
                f"precursor '{prec.name}': default value used ({note}) — request a mill EPD "
                f"to replace it with actual data")
            if used_fallback:
                needs_attention.append(
                    f"precursor '{prec.name}': {prec.country} has NO default value for CN "
                    f"{prec.cn_code}, so the Annex I fallback applies — the average of the "
                    f"ten highest-intensity exporting countries (Q&A p.37). A mill EPD is "
                    f"worth more here than for any other input.")

        contrib_unc = math.hypot(ratio_unc, psd_unc)
        dir_terms.append((ratio * psd, contrib_unc))
        ind_terms.append((ratio * psi, contrib_unc))
        elec_terms.append((ratio * pse, contrib_unc))
        prec_lines.append({
            "precursor": prec.name, "cn_code": prec.cn_code, "mass_t": prec.mass_t,
            "ratio_t_per_t": ratio,
            "see_direct_used": Line(psd, source, psd_unc, note).__dict__,
            "see_indirect_used": Line(psi, source, psd_unc).__dict__,
        })

    see_dir = sum(v for v, _ in dir_terms)
    see_ind = sum(v for v, _ in ind_terms)
    emb_elec = sum(v for v, _ in elec_terms)
    # Recorded, never capped: defaults are lawful without limit (IR 2025/2547 Annex II
    # A.1.2); the emissions report only discloses this share (Annex IV — docs/15 §8.1).
    share_default = default_dir_sum / see_dir if see_dir else 0.0

    dir_source = "actual" if share_default == 0.0 else ("mixed" if any_actual_prec or se_dir_own else "default")
    return ProductSEE(
        product_name=p.name,
        cn_code=p.cn_code,
        invoice_name=p.invoice_name,
        see_direct=Line(see_dir, dir_source if dir_source != "mixed" else "actual",
                        _combine_rel(*dir_terms),
                        note="includes default-value precursor share" if share_default else ""),
        see_indirect=Line(see_ind, "actual", _combine_rel(*ind_terms),
                          note=("recorded; part of the certificate obligation for this sector"
                                if indirect_in_certificate(p.cn_code) else
                                f"recorded; NOT in the CN {p.cn_code.replace(' ', '')[:4]} "
                                f"certificate obligation")),
        see_total=Line(see_dir + see_ind, "actual" if share_default == 0 else "mixed",
                       _combine_rel(*(dir_terms + ind_terms))),
        embedded_electricity_mwh_per_t=Line(emb_elec, "actual", _combine_rel(*elec_terms)),
        share_default_values=share_default,
        precursor_lines=prec_lines,
        needs_attention=needs_attention,
    )


def compute_installation(processes: list[ProcessInput], period_year: int) -> list[ProductSEE]:
    """One SEE per CN good for the determination period (the annual artifact)."""
    return [compute_product_see(p, period_year) for p in processes]
