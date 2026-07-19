#!/usr/bin/env python3
"""LINE-bot simulator: the FOUR SIGHTS from one photo set, end-to-end, no channel.

Posts fake (but correctly signed, when a secret is set) LINE events against a
running `carbonpass serve` instance, using the firm_a corpus. One session, in
sequence (docs/archive/21 §1.5 — this is the demo-video script):

    (photographs two Taipower bills)      the one photograph
    「狀態」                                what's been received
    「產生報告」   Sight ① product carbon:  CBAM pack + ranked fix-list
    「浪費」       Sight ② material loss:   waste map, gross AND net, drift
    「排程」       Sight ③ energy timing:   grid-aware shift plan
    「我正常嗎」   Sight ④ peer position:   percentile vs (labelled) seed band

Usage:
    uv run python -m carbonpass serve &          # terminal 1
    uv run python scripts/line_simulator.py      # terminal 2
    (--fast skips 「產生報告」, whose VLM pass takes minutes; the other three
     sights run on structured documents and stay fast)
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import hmac
import json
import os
from pathlib import Path

import httpx

REPO = Path(__file__).resolve().parents[1]
BASE = os.environ.get("CARBONPASS_URL", "http://127.0.0.1:8787")
USER = "U_simulated_owner_001"


def sign(body: bytes) -> dict:
    secret = os.environ.get("LINE_CHANNEL_SECRET", "").strip()
    if not secret:
        return {}
    mac = hmac.new(secret.encode(), body, hashlib.sha256).digest()
    return {"X-Line-Signature": base64.b64encode(mac).decode()}


def post_events(events: list[dict]) -> list[dict]:
    body = json.dumps({"destination": "simulator", "events": events}).encode()
    r = httpx.post(f"{BASE}/line/webhook", content=body,
                   headers={"Content-Type": "application/json", **sign(body)},
                   timeout=1800.0)
    r.raise_for_status()
    return r.json().get("replies", [])


def image_event(path: Path) -> dict:
    return {"type": "message", "replyToken": "rt", "source": {"userId": USER},
            "message": {"type": "image", "id": "sim", "_local_path": str(path),
                        "fileName": path.name}}


def text_event(text: str) -> dict:
    return {"type": "message", "replyToken": "rt", "source": {"userId": USER},
            "message": {"type": "text", "text": text}}


def show(replies: list[dict]) -> None:
    for rep in replies:
        for t in rep["texts"]:
            print("🤖", t.replace("\n", "\n   "), "\n")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fast", action="store_true", help="skip the VLM report step")
    args = ap.parse_args()

    bills = sorted((REPO / "data/mock_corpus/firm_a/bills").glob("*.png"))
    if not bills:
        print("corpus missing — run scripts/make_mock_corpus.py")
        return 1

    print("👤 (photographs two Taipower bills)")
    show(post_events([image_event(bills[0]), image_event(bills[6])]))
    print("👤 狀態")
    show(post_events([text_event("狀態")]))
    if not args.fast:
        print("👤 產生報告   — Sight ① product carbon (VLM parses the photos; takes a while)")
        show(post_events([text_event("產生報告")]))
    else:
        print("(--fast: skipping 「產生報告」 / Sight ① — VLM step)")
    print("👤 浪費       — Sight ② material loss (gross AND net)")
    show(post_events([text_event("浪費")]))
    print("👤 排程       — Sight ③ energy timing")
    show(post_events([text_event("排程")]))
    print("👤 我正常嗎   — Sight ④ peer position (synthetic seed, labelled)")
    show(post_events([text_event("我正常嗎")]))
    print("four sights done ✓  (real channel = set LINE_CHANNEL_SECRET/"
          "LINE_CHANNEL_ACCESS_TOKEN in .env and point the LINE console at /line/webhook)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
