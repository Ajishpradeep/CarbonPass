# CarbonPass — Engineer Handoff & Claude Code Kickoff

**This file reflects the ACTUAL current state of the repo, not a fresh-start guide.** Read it with:
- `docs/10_poc_blueprint.md` — technical spec (architecture, stack, data sources, CBAM reality in §2A, gaps)
- `docs/09_master_proposal.md` — product concept and rationale
- `docs/00_session_handoff.md` — verified facts + kill-list (claims that are WRONG — never reintroduce)

Repo root: `/Users/pardeep/code/Personal/CarbonPass` · Last synced: 16 Jul 2026

---

## 0. Where the project stands right now

**Done (prepared and verified):**
- Git repo + `uv` venv initialized; `pyproject.toml`, `.gitignore` (ignores `.env`, `.venv`, `.DS_Store`, `data/mock_corpus/`), `.env` (holds `MOENV_API_KEY`), `.env.example`.
- **All EU CBAM official material downloaded** into `data/cbam_official/` (template, filled examples incl. screws & nuts, default values, benchmarks, guidance EN+ZH, Q&A).
- **The "screws and nuts" answer key is present and validated** — 19-sheet workbook, structurally identical to the blank template (this is the Sprint-0 map).
- **MOENV emission-coefficient snapshot** in `data/ef/moenv_coefficients.json` (currently 1,000 rows — may be truncated; refresh with the new fetcher below).
- Four handoff docs copied into `docs/`; two proposal PDFs alongside.
- **`scripts/pull_moenv_ef.py`** — full-pagination MOENV fetcher with static-file fallback (added this session).

**Still to do before/at the coding session (2 min):**
1. `ollama pull qwen3-vl:8b-instruct` (and `qwen3-vl:4b-instruct` for CPU fallback) — not yet pulled.
2. Refresh the coefficient table to full size: `python scripts/pull_moenv_ef.py` (see §3).
3. *(Decision)* Python is currently **3.10** (`.python-version`, `pyproject`). Blueprint targets **3.11**; Docling/some tooling prefer it. Either bump to 3.11 and recreate the venv, or proceed on 3.10 knowingly.
4. LINE Messaging API channel — only needed when Module 3 (bot) is built, not for Sprint 0–1.

**Built by the Claude Code agent (correctly absent now):** `schema/`, `src/carbonpass/`, `tests/`, `data/mock_corpus/`, and the rest of `scripts/`.

---

## 1. Repo layout — actual current state

```
CarbonPass/
├─ README.md                     [stub — agent fills]
├─ pyproject.toml                [deps empty — agent adds]
├─ main.py                       [uv stub — agent replaces]
├─ .env                          [has MOENV_API_KEY]           OK
├─ .env.example                  [template: LINE, Ollama, paths] OK
├─ .gitignore .python-version .venv/                            OK
├─ docs/
│  ├─ 00_session_handoff.md  09_master_proposal.md              OK
│  ├─ 10_poc_blueprint.md    11_setup_kickoff.md  (this file)   OK
│  └─ CarbonPass *.pdf  (Educational + Submission proposals)    OK
├─ data/
│  ├─ cbam_official/
│  │  ├─ communication_template.xlsx        [renamed to this]   OK
│  │  ├─ default_values.xlsx  benchmarks.xlsx  cbam_qa.pdf      OK
│  │  ├─ guidance_installations_outside_eu_EN.pdf / _ZH.pdf     OK
│  │  ├─ template_examples.zip                                  OK
│  │  └─ template_examples/
│  │     ├─ 4 CBAM SEE V2.1_Example Steel 3 Screws and nuts_final.xlsx  <- ANSWER KEY  OK
│  │     └─ (cement, 2x steel, fertilizer, aluminium, hydrogen) OK
│  ├─ ef/moenv_coefficients.json            [1000 rows — refresh] OK
│  └─ mock_corpus/                          [agent generates]
├─ scripts/
│  └─ pull_moenv_ef.py                       [added this session] OK
├─ schema/        [agent: cbam_template_map.yaml, *.schema.json]
├─ src/carbonpass/  [agent: ingestion, egui, allocation, rules, writer, costdelta, scheduler, api, line_bot]
└─ tests/golden/  [agent: reproduce screws&nuts SEE]
```

---

## 2. The target schema is already known (from the validated workbook)

The blank template and the screws-and-nuts example share these **19 sheets** — these are the fields the writer must fill and the rules engine must satisfy. Sprint 0 transcribes the exact cell map from the example into `schema/cbam_template_map.yaml`:

`0_Versions` · `a_Contents` · `b_Guidelines&Conditions` · `c_CodeLists` · **`A_InstData`** (installation) · **`B_EmInst`** (emissions of installation) · **`C_Emissions&Energy`** · **`D_Processes`** · **`E_PurchPrec`** (purchased precursors ← the steel wire-rod SEE) · `F_Tools` · `G_FurtherGuidance` · `Summary_Processes` · **`Summary_Products`** (per-CN-code SEE output) · **`Summary_Communication`** (what goes to the importer) · `InputOutput` · `Parameters_Constants` · **`Parameters_CNCodes`** · `Translations` · `VersionDocumentation`.

---

## 3. Refresh the coefficient table (run this)

```bash
cd /Users/pardeep/code/Personal/CarbonPass
python scripts/pull_moenv_ef.py            # uses MOENV_API_KEY from .env; paginates all rows
# fallback if the API 500s / dataset empty: it keeps the current snapshot and prints a manual link.
```
Fields per record: `name` (係數名稱), `coe` (kgCO₂e), `unit`, `departmentname`, `announcementyear`. Row 1 today is `合金鋼鋼胚（機械五金用）` (alloy steel billet for hardware) — a direct fastener-precursor factor.

---

## 4. Start commands (copy-paste)

```bash
cd /Users/pardeep/code/Personal/CarbonPass
ollama pull qwen3-vl:8b-instruct && ollama pull qwen3-vl:4b-instruct
python scripts/pull_moenv_ef.py            # full coefficient snapshot
# then open Claude Code in this repo and paste the prompt in §5
```

---

## 5. The Claude Code kickoff prompt (paste this, inside the repo)

```
You are the lead engineer building the CarbonPass PoC. The repo is already prepared (docs,
CBAM official data, MOENV coefficients, .env). Before writing code, read these in full and treat
them as source of truth:
  - docs/10_poc_blueprint.md   (technical spec — architecture, stack, data, and §2A "how CBAM
                                actually works": period/cadence/allocation — obey it)
  - docs/09_master_proposal.md (product concept)
  - docs/00_session_handoff.md (verified facts + a KILL-LIST of wrong claims — never reintroduce)
  - docs/11_setup_kickoff.md   (current repo state, target schema, Definition of Done)

PROJECT IN ONE LINE: a local-first AI that turns a Taiwanese fastener SME's photographed
documents (Taipower bill, steel wire-rod e-invoices, production log) into a verifier-ready EU CBAM
"Communication Template for installations" (.xlsx) for CN 7318 goods, plus a default-vs-actual
buyer-cost screen. Focus now is Module 1; Module 2 (grid scheduler) and Module 3 (LINE bot) come later.

NON-NEGOTIABLE CBAM RULES (docs/10 §2A — get these right or you solve the wrong problem):
  - It is PER-PRODUCT-PER-YEAR, never per-shipment. Compute one SEE (tCO2e/tonne) per CN code per
    determination period (calendar year); the importer reuses it across shipments.
  - Output = the producer->importer Communication Template, NOT the EU Registry declaration.
  - For fasteners (complex good) the dominant input is the PURCHASED STEEL precursor, then direct
    fuel, then production volumes, then electricity. Electricity is indirect and NOT in the CN 7318
    certificate — don't overweight it.
  - Precursor SEE: mill EPD if supplied, else CBAM default (data/cbam_official/default_values.xlsx)
    as conservative fallback, with the correct year mark-up (10/20/30%).
  - Every emitted figure carries a source flag (actual/default) + per-line uncertainty. The tool
    PREPARES verification; it never certifies.

STACK (chosen — don't re-litigate): Python (repo is 3.10; 3.11 acceptable); Ollama serving
qwen3-vl:8b-instruct (vLLM + guided_json later for scale); Docling layout pre-pass; PaddleOCR-VL /
DeepSeek-OCR numeric backstop; OR-Tools MILP + NumPy Monte-Carlo for allocation-with-uncertainty;
openpyxl to fill the template; FastAPI; LINE Messaging API for the front end. Only approved VLM
challenger to benchmark against is InternVL3.5-8B.

KEY ASSETS ALREADY IN THE REPO:
  - Target schema + answer key: data/cbam_official/template_examples/"4 CBAM SEE V2.1_Example
    Steel 3 Screws and nuts_final.xlsx" (19 sheets; see docs/11 §2). Blank: data/cbam_official/
    communication_template.xlsx
  - Default values: data/cbam_official/default_values.xlsx  · Emission factors: data/ef/
    moenv_coefficients.json (run scripts/pull_moenv_ef.py first to ensure it's the full table)

DO THIS SESSION, in order, committing after each step:
  1. Run `python scripts/pull_moenv_ef.py` to refresh the full coefficient table. Then scaffold the
     repo per docs/11 §1 (packages under src/carbonpass/, schema/, tests/, add deps to pyproject).
     Confirm `uv sync` / install works.
  2. Open the screws-and-nuts workbook and the blank communication_template.xlsx. Transcribe the
     exact sheets/cells we must fill into schema/cbam_template_map.yaml, and capture the worked SEE
     numbers as golden expected output in tests/golden/.
  3. scripts/make_mock_corpus.py -> 3 firms: Taipower TOU bills (realistic layout), MIG 4.0
     e-invoices (steel/gas/plating) via the open Turnkey format, per-CN-code production logs ->
     data/mock_corpus/{firm_a,firm_b,firm_c}/ + ground_truth.json (hand-computed SEE).
  4. src/carbonpass/ingestion: Docling pre-pass -> qwen3-vl:8b-instruct (Ollama) -> activity_data JSON
     validated against schema/activity_data.schema.json. Run Firm A end-to-end.
  5. src/carbonpass/allocation (OR-Tools + Monte-Carlo) and src/carbonpass/rules (SEE per IR
     2025/2547 + default fallback + mark-up). tests/golden must reproduce the screws&nuts numbers
     within tolerance.
  6. src/carbonpass/writer (openpyxl -> fill communication_template.xlsx with actual/default/
     needs-attention flags) + src/carbonpass/costdelta (buyer screen).
  7. Update README with run commands. Report status vs the Definition of Done (§6) and list blockers.

Ask me before: changing the model/stack, adding a paid dependency, or anything implying
per-shipment carbon logic. Otherwise proceed autonomously; keep commits small.
```

---

## 6. Definition of Done (kickoff session)
1. Repo scaffolded per §1; deps install cleanly.
2. `schema/cbam_template_map.yaml` transcribed from the screws & nuts workbook + golden expected JSON.
3. Mock corpus for 3 firms (Taipower bills + MIG 4.0 e-invoices + production logs + `ground_truth.json`).
4. Ingestion runs Firm A end-to-end: photo/PDF → validated `activity_data` JSON via `qwen3-vl:8b-instruct`.
5. Rules engine reproduces the screws & nuts SEE within tolerance (pytest green).
6. `writer` emits a filled `communication_template.xlsx` for Firm A with source/uncertainty flags.
7. README documents run commands.

---

## 7. Pre-flight checklist
- [x] New `carbonpass/` repo created, `git init`, venv
- [x] Four handoff `.md` files in `docs/`
- [x] EU CBAM files in `data/cbam_official/`; examples unzipped; template renamed `communication_template.xlsx`
- [x] MOENV coefficients snapshot in `data/ef/` (refresh with fetcher for full table)
- [x] `scripts/pull_moenv_ef.py` present
- [x] `.env` (MOENV key) + `.env.example`
- [ ] `ollama pull qwen3-vl:8b-instruct` (+ `:4b-instruct`)
- [ ] `python scripts/pull_moenv_ef.py` run for the full table
- [ ] Python 3.10 vs 3.11 decision made
- [ ] LINE Messaging API channel (only before Module 3)
- [ ] Paste §5 prompt into Claude Code inside the repo
