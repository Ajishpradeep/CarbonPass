"""Central configuration: paths, environment, and CBAM constants."""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# --- repo paths -------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = REPO_ROOT / "data"
CBAM_OFFICIAL_DIR = DATA_DIR / "cbam_official"
BLANK_TEMPLATE = CBAM_OFFICIAL_DIR / "communication_template.xlsx"
DEFAULT_VALUES_XLSX = CBAM_OFFICIAL_DIR / "default_values.xlsx"
ANSWER_KEY_XLSX = (
    CBAM_OFFICIAL_DIR
    / "template_examples"
    / "4 CBAM SEE V2.1_Example Steel 3 Screws and nuts_final.xlsx"
)
MOENV_EF_JSON = DATA_DIR / "ef" / "moenv_coefficients.json"
MOCK_CORPUS_DIR = DATA_DIR / "mock_corpus"
SCHEMA_DIR = REPO_ROOT / "schema"
TEMPLATE_MAP_YAML = SCHEMA_DIR / "cbam_template_map.yaml"
ACTIVITY_SCHEMA_JSON = SCHEMA_DIR / "activity_data.schema.json"
OUT_DIR = REPO_ROOT / "out"

# --- Ollama / VLM -----------------------------------------------------------
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "qwen3-vl:8b-instruct")

# --- CBAM constants (sources: docs/10 §2, docs/00 §3) ------------------------
# NOTE (Sprint 2): the default-value mark-up is NEVER a constant — it is derived
# from the workbook row itself (`DefaultValue.derived_markup()`: steel 10/20/30%,
# fertilisers flat 1% — docs/15 §6 defects 1–2). Certificate prices live in
# data/prices.yaml (carbonpass.prices) and the grid EF in data/ef/grid_ef.yaml
# (carbonpass.rules.gridef): dated config, never literals (docs/21 §2.8).

# TEMPORARY — removed by the defect-3/defect-7 commits in this sprint:
CERTIFICATE_PRICE_EUR = {"2026Q1": 75.36, "2026Q2": 75.28}
GRID_EF_KGCO2_PER_KWH = 0.474

# Indirect emissions are recorded in the template but are NOT part of the
# CN 7318 (iron & steel) certificate obligation — only cement & fertiliser
# include indirect today (docs/10 §2A, G7). Do not fold indirect into the
# certificate cost for fasteners.
INDIRECT_IN_CERTIFICATE_SECTORS = {"cement", "fertiliser"}

# CN chapter/prefix -> sector key (longest prefix wins).
CN_SECTOR_PREFIXES = {
    "25": "cement",
    "2808": "fertiliser", "2814": "fertiliser", "28342": "fertiliser",
    "31": "fertiliser",
    "2804": "hydrogen",
    "72": "iron_steel", "73": "iron_steel",
    "76": "aluminium",
}


def sector_for_cn(cn_code: str) -> str:
    """Sector key for a CN code (longest-prefix match); raises on unmapped codes."""
    cn = cn_code.replace(" ", "")
    best = ""
    for prefix, sector in CN_SECTOR_PREFIXES.items():
        if cn.startswith(prefix) and len(prefix) > len(best):
            best = prefix
    if not best:
        raise KeyError(f"CN {cn_code!r}: no CBAM sector mapping — extend CN_SECTOR_PREFIXES")
    return CN_SECTOR_PREFIXES[best]


def indirect_in_certificate(cn_code: str) -> bool:
    """Whether indirect (electricity) emissions are inside the certificate obligation."""
    return sector_for_cn(cn_code) in INDIRECT_IN_CERTIFICATE_SECTORS
