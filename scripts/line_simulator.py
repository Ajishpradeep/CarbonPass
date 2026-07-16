#!/usr/bin/env python3
"""LINE-bot simulator: drives the webhook end-to-end without a LINE channel.

Posts fake (but correctly signed, when a secret is set) LINE events against a
running `carbonpass serve` instance, using the firm_a corpus: two bill photos
in, then 「狀態」, 「產生報告」 and 「排程」. Prints every bot reply.

Usage:
    uv run python -m carbonpass serve &          # terminal 1
    uv run python scripts/line_simulator.py      # terminal 2
    (--fast skips 「產生報告」, whose VLM pass takes minutes)
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
    print("👤 排程")
    show(post_events([text_event("排程")]))
    if not args.fast:
        print("👤 產生報告   (VLM parses the received photos — takes a while)")
        show(post_events([text_event("產生報告")]))
    print("simulator done ✓  (real channel = set LINE_CHANNEL_SECRET/"
          "LINE_CHANNEL_ACCESS_TOKEN in .env and point the LINE console at /line/webhook)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
