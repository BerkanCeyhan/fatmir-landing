#!/usr/bin/env python3
"""Gewaehlte Varianten aus gen/ freistellen und als WebP nach img2/ legen.

    uv run --with pillow --with numpy python scripts/neu-bilder.py

Der flache Hintergrund wird per Color-to-Alpha transparent (wie in GIMP):
Linien und rote Flaechen bleiben, die Kanten behalten ihre Kantenglaettung.
So sitzen die Bilder auf Creme, Sand und Ink ohne sichtbares Rechteck.
"""
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
PICKS = {
    "neu-live-1": ("neu-live", 1100),
    "neu-handel-2": ("neu-handel", 1000),
    "neu-marketing-2": ("neu-marketing", 1000),
    "neu-coaching-1": ("neu-coaching", 1000),
    "neu-award-1": ("neu-award", 1200),
}


def color_to_alpha(rgb, bg):
    p = rgb.astype(np.float64) / 255.0
    b = np.array(bg, dtype=np.float64) / 255.0
    up = np.where(p > b, (p - b) / np.maximum(1.0 - b, 1e-6), 0.0)
    down = np.where(p < b, (b - p) / np.maximum(b, 1e-6), 0.0)
    alpha = np.clip(np.max(np.maximum(up, down), axis=2), 0.0, 1.0)
    # leises Rauschen im Grund wegschneiden, Rest auf volle Deckkraft strecken
    alpha = np.clip((alpha - 0.18) / 0.82, 0.0, 1.0)
    a = alpha[..., None]
    color = np.where(a > 1e-4, (p - b) / np.maximum(a, 1e-4) + b, 0.0)
    out = np.dstack([np.clip(color, 0, 1), alpha])
    return Image.fromarray((out * 255 + 0.5).astype(np.uint8), "RGBA")


for src, (name, width) in PICKS.items():
    im = Image.open(ROOT / "gen" / f"{src}.raw").convert("RGB")
    arr = np.asarray(im)
    # Hintergrund aus den vier Ecken schaetzen
    corners = np.concatenate([arr[:24, :24].reshape(-1, 3), arr[:24, -24:].reshape(-1, 3),
                              arr[-24:, :24].reshape(-1, 3), arr[-24:, -24:].reshape(-1, 3)])
    bg = tuple(int(v) for v in np.median(corners, axis=0))
    rgba = color_to_alpha(arr, bg)
    h = round(rgba.height * width / rgba.width)
    rgba = rgba.resize((width, h), Image.LANCZOS)
    out = ROOT / "img2" / f"{name}.webp"
    rgba.save(out, "WEBP", quality=84, alpha_quality=70, method=6)
    print(f"{name}: Grund {bg}, {width}x{h}, {out.stat().st_size // 1024} KB")
