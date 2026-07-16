"""Module 3 API tests — TestClient, no network, no VLM (fast paths only)."""
from __future__ import annotations

import base64
import hashlib
import hmac
import json

import pytest
from fastapi.testclient import TestClient

from carbonpass.api.app import app

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok" and "ollama" in body


def test_ingest_404_on_missing_firm():
    r = client.post("/ingest", json={"firm_dir": "does/not/exist"})
    assert r.status_code == 404


def test_webhook_signature_rejected_when_secret_set(monkeypatch):
    monkeypatch.setenv("LINE_CHANNEL_SECRET", "topsecret")
    body = json.dumps({"events": []}).encode()
    r = client.post("/line/webhook", content=body,
                    headers={"Content-Type": "application/json",
                             "X-Line-Signature": "bogus"})
    assert r.status_code == 403


def test_webhook_signature_accepted_when_valid(monkeypatch):
    secret = "topsecret"
    monkeypatch.setenv("LINE_CHANNEL_SECRET", secret)
    body = json.dumps({"events": []}).encode()
    sig = base64.b64encode(hmac.new(secret.encode(), body, hashlib.sha256).digest()).decode()
    r = client.post("/line/webhook", content=body,
                    headers={"Content-Type": "application/json", "X-Line-Signature": sig})
    assert r.status_code == 200 and r.json()["ok"] is True


def test_webhook_simulator_mode_text_flow(monkeypatch, tmp_path):
    monkeypatch.delenv("LINE_CHANNEL_SECRET", raising=False)
    monkeypatch.delenv("LINE_CHANNEL_ACCESS_TOKEN", raising=False)
    monkeypatch.chdir(tmp_path)  # session folders land under tmp out/
    body = json.dumps({"events": [{
        "type": "message", "replyToken": "rt",
        "source": {"userId": "U_test"},
        "message": {"type": "text", "text": "你好"},
    }]}).encode()
    r = client.post("/line/webhook", content=body,
                    headers={"Content-Type": "application/json"})
    assert r.status_code == 200
    replies = r.json()["replies"]
    assert replies and "CarbonPass" in replies[0]["texts"][0]


@pytest.mark.skipif(not __import__("pathlib").Path("data/mock_corpus/firm_a/firm.json").exists(),
                    reason="corpus not generated")
def test_schedule_endpoint_runs():
    r = client.post("/schedule", json={"firm_dir": "data/mock_corpus/firm_a", "month": 7})
    assert r.status_code == 200
    led = r.json()["ledger"]
    assert led["delta_week"]["cost_ntd"] >= 0
    assert "not" in " ".join(r.json()["honesty"]).lower()  # G7 wording present
