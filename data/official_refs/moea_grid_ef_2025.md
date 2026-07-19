# MOEA Energy Administration — 2025 (民國114) electricity emission factors
**Fetched:** 19 Jul 2026 · **Announced:** 2 Jun 2026 · **Source (verbatim page saved from):**
https://www.moea.gov.tw/MNS/populace/news/News.aspx?kind=1&menu_id=40&news_id=122891

Key figures (公用售電業電力排碳係數, kgCO2e/kWh):
- **Overall: 0.467** (−1.5% vs 2024's 0.474; −12% vs 2016)
- **Industrial (產業電力排碳係數): 0.466** ← first year this split exists; intended for corporate
  inventory/disclosure use — the correct factor for CarbonPass factories
- Residential (民生住宅, 表燈非營業): 0.471
- National factor incl. private green-power direct/wheeling (全國電力排放係數), 2025 est.: **0.456**

Key sentence (translated): "From 2025 the Energy Administration additionally publishes an
'industry electricity emission factor' of 0.466 kgCO2e/kWh for enterprises to use in emissions
inventory and disclosure, helping industry align with international carbon-reduction requirements."

Engine rule: select factor by (year, series=industrial), carry provenance string in every output.
Config: `data/ef/grid_ef.yaml`.
