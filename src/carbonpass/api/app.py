"""Module 3 API surface: FastAPI wrappers over the Module 1/2 pipeline + LINE webhook.

Local-first: this server runs on the factory's own machine; only the outputs the
owner chooses to send (the .xlsx pack) ever leave. Start with:
    uv run python -m carbonpass serve            # http://127.0.0.1:8787
"""
from __future__ import annotations

import json
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from carbonpass import __version__

app = FastAPI(title="CarbonPass", version=__version__,
              description="Local-first CBAM data-pack engine (Module 1) + "
                          "grid-aware scheduler (Module 2) + LINE webhook (Module 3)")


class IngestRequest(BaseModel):
    firm_dir: str
    use_vlm: bool = True


class PackRequest(BaseModel):
    activity_json: str
    output: str | None = None


class ScheduleRequest(BaseModel):
    firm_dir: str
    month: int = 7


@app.get("/health")
def health() -> dict:
    from carbonpass.ingestion.vlm import ollama_available

    return {"status": "ok", "version": __version__, "ollama": ollama_available()}


@app.post("/ingest")
def ingest(req: IngestRequest) -> dict:
    from carbonpass.ingestion.pipeline import ingest_firm

    firm = Path(req.firm_dir)
    if not (firm / "firm.json").exists():
        raise HTTPException(404, f"no firm.json under {firm}")
    activity = ingest_firm(firm, use_vlm=req.use_vlm)
    out = Path("out") / f"{firm.name}_activity.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(activity, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"activity_json": str(out), "documents": len(activity["documents"])}


@app.post("/pack")
def pack(req: PackRequest) -> dict:
    from carbonpass.writer.fill import fill_template
    from carbonpass.pack import load_activity

    src = Path(req.activity_json)
    if not src.exists():
        raise HTTPException(404, f"{src} not found")
    out = Path(req.output) if req.output else \
        Path("out") / f"{src.stem.replace('_activity', '')}_communication_template.xlsx"
    sidecar = fill_template(load_activity(src), out)
    return {"xlsx": str(out), "flags_json": str(out.with_suffix(".flags.json")),
            "products": sidecar["products"], "needs_attention": sidecar["needs_attention"]}


@app.get("/fixlist")
def fixlist_route(activity_json: str, firm_dir: str) -> dict:
    """Ranked fix-list (replaces /costdelta): yield → mill EPD → process energy →
    load shifting, each able to answer 'not worth it this year'."""
    from carbonpass.costdelta.fixlist import fixlist

    src = Path(activity_json)
    if not src.exists():
        raise HTTPException(404, f"{src} not found")
    if not Path(firm_dir).exists():
        raise HTTPException(404, f"{firm_dir} not found")
    return fixlist(str(src), firm_dir)


class WasteRequest(BaseModel):
    activity_json: str
    firm_dir: str


@app.post("/waste")
def waste(req: WasteRequest) -> dict:
    """Sight ②: per-line waste map (gross AND net) + monthly drift series."""
    from carbonpass.pack import load_activity
    from carbonpass.waste import monthly_series, scan as waste_scan

    src = Path(req.activity_json)
    if not src.exists():
        raise HTTPException(404, f"{src} not found")
    if not Path(req.firm_dir).exists():
        raise HTTPException(404, f"{req.firm_dir} not found")
    r = waste_scan(str(src), req.firm_dir)
    r["drift"] = monthly_series(req.firm_dir, load_activity(src))
    return r


@app.post("/schedule")
def schedule(req: ScheduleRequest) -> dict:
    from carbonpass.scheduler.ledger import schedule_firm

    firm = Path(req.firm_dir)
    if not (firm / "firm.json").exists():
        raise HTTPException(404, f"no firm.json under {firm}")
    return schedule_firm(firm, month=req.month)


# LINE webhook router (Module 3 front end)
from carbonpass.line_bot.webhook import router as line_router  # noqa: E402

app.include_router(line_router)
