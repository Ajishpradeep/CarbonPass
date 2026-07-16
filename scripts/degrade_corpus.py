#!/usr/bin/env python3
"""Phone-photo degradation of the clean mock corpus, for the Sprint-1 VLM bake-off.

Clean renders overstate real-world accuracy: owners photograph bills tilted, in
factory light, with cheap phones. This script produces deterministic degraded
variants of each PNG so the bake-off measures robustness, not best-case OCR.

Variants (docs/10 §6.2 — blur/tilt/low-light robustness is a selection criterion):
    rot    ±3–7° rotation, white fill (tilted photo)
    blur   gaussian radius 1.5–2.5 (focus miss)
    dark   brightness 0.45 × contrast 0.7 (factory-floor light)
    jpeg   quality-30 re-encode (messaging-app compression)
    warp   ~2% perspective distortion (off-axis shot)
    combo  rot + dark + jpeg (the realistic worst case)

Output: data/mock_corpus/degraded/<firm>/<variant>/<original name>.png  (gitignored)

Usage: python scripts/degrade_corpus.py [--firm firm_a] [--bills-only]
"""
from __future__ import annotations

import argparse
import io
import random
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter

REPO = Path(__file__).resolve().parents[1]
CORPUS = REPO / "data" / "mock_corpus"
OUT = CORPUS / "degraded"


def v_rot(img: Image.Image, rng: random.Random) -> Image.Image:
    angle = rng.choice([-1, 1]) * rng.uniform(3, 7)
    return img.rotate(angle, expand=True, fillcolor="white", resample=Image.BICUBIC)


def v_blur(img: Image.Image, rng: random.Random) -> Image.Image:
    return img.filter(ImageFilter.GaussianBlur(radius=rng.uniform(1.5, 2.5)))


def v_dark(img: Image.Image, rng: random.Random) -> Image.Image:
    img = ImageEnhance.Brightness(img).enhance(0.45)
    return ImageEnhance.Contrast(img).enhance(0.7)


def v_jpeg(img: Image.Image, rng: random.Random) -> Image.Image:
    buf = io.BytesIO()
    img.convert("RGB").save(buf, "JPEG", quality=30)
    buf.seek(0)
    return Image.open(buf).convert("RGB")


def v_warp(img: Image.Image, rng: random.Random) -> Image.Image:
    w, h = img.size
    d = 0.02
    # slight keystone: top edge pinched
    coeffs = _persp_coeffs(
        [(0, 0), (w, 0), (w, h), (0, h)],
        [(w * d, h * d * 0.5), (w * (1 - d), 0), (w, h), (0, h * (1 - d * 0.5))])
    return img.transform((w, h), Image.PERSPECTIVE, coeffs,
                         Image.BICUBIC, fillcolor="white")


def v_combo(img: Image.Image, rng: random.Random) -> Image.Image:
    return v_jpeg(v_dark(v_rot(img, rng), rng), rng)


def _persp_coeffs(src, dst):
    # solve the 8-param perspective transform (PIL wants dst->src mapping)
    import numpy as np

    A, B = [], []
    for (x, y), (u, v) in zip(dst, src):
        A.append([x, y, 1, 0, 0, 0, -u * x, -u * y])
        A.append([0, 0, 0, x, y, 1, -v * x, -v * y])
        B += [u, v]
    return tuple(np.linalg.solve(np.array(A, dtype=float), np.array(B, dtype=float)))


VARIANTS = {"rot": v_rot, "blur": v_blur, "dark": v_dark,
            "jpeg": v_jpeg, "warp": v_warp, "combo": v_combo}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--firm", default="firm_a")
    ap.add_argument("--bills-only", action="store_true")
    args = ap.parse_args()

    firm_dir = CORPUS / args.firm
    sources = sorted((firm_dir / "bills").glob("*.png"))
    if not args.bills_only:
        sources += sorted((firm_dir / "invoices").glob("*.png"))[:6]
        if (firm_dir / "production_log.png").exists():
            sources.append(firm_dir / "production_log.png")
    if not sources:
        print("no source PNGs — run scripts/make_mock_corpus.py first")
        return 1

    n = 0
    for name, fn in VARIANTS.items():
        outdir = OUT / args.firm / name
        outdir.mkdir(parents=True, exist_ok=True)
        for src in sources:
            rng = random.Random(f"{name}:{src.name}")   # per-file deterministic
            img = Image.open(src).convert("RGB")
            fn(img, rng).save(outdir / src.name)
            n += 1
    print(f"OK: {n} degraded images -> {OUT / args.firm} ({len(VARIANTS)} variants × {len(sources)} sources)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
