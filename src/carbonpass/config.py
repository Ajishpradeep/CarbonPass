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
# Default-value mark-up for iron & steel when actual data unavailable.
DEFAULT_MARKUP_BY_YEAR = {2026: 0.10, 2027: 0.20, 2028: 0.30}  # 2028 onward

# Official quarterly CBAM certificate prices, EUR/tCO2e (C13).
CERTIFICATE_PRICE_EUR = {"2026Q1": 75.36, "2026Q2": 75.28}

# Taiwan grid electricity emission factor, kgCO2e/kWh (MOEA Energy Admin, 2024).
GRID_EF_KGCO2_PER_KWH = 0.474

# Indirect emissions are recorded in the template but are NOT part of the
# CN 7318 (iron & steel) certificate obligation — only cement & fertiliser
# include indirect today (docs/10 §2A, G7). Do not fold indirect into the
# certificate cost for fasteners.
INDIRECT_IN_CERTIFICATE_SECTORS = {"cement", "fertiliser"}


def markup_for_year(year: int) -> float:
    """Default-value mark-up for a determination period (10/20/30%, 2028 onward capped at 30%)."""
    if year <= 2026:
        return DEFAULT_MARKUP_BY_YEAR[2026]
    return DEFAULT_MARKUP_BY_YEAR.get(year, DEFAULT_MARKUP_BY_YEAR[2028])
