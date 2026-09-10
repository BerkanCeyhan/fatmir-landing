#!/usr/bin/env python3
"""Zieht Vertex- und Fragment-Shader aus den React-Bits-Hintergruenden.

    python3 scripts/extract-shaders.py

Liest /tmp/rb-<Name>.jsx und schreibt gen/shaders.json.
"""
import json
import re
from pathlib import Path

NAMES = ["Aurora", "Iridescence", "LiquidChrome", "Balatro", "Grainient",
         "LineWaves", "SlicedWaves", "Topography", "SoftAurora", "Plasma"]

OUT = Path("gen/shaders.json")
result = {}

for name in NAMES:
    src = Path(f"/tmp/rb-{name}.jsx").read_text(encoding="utf-8")
    literals = re.findall(r"`([^`]*)`", src, re.S)
    shaders = [t for t in literals if "void main" in t]
    vert = next((t for t in shaders if "gl_Position" in t), None)
    frag = next((t for t in shaders if t is not vert and
                 ("gl_FragColor" in t or "fragColor" in t or "outColor" in t)), None)
    if not vert or not frag:
        print(f"{name}: uebersprungen (vert={bool(vert)} frag={bool(frag)})")
        continue

    uni = re.search(r"uniforms:\s*\{(.*?)\n\s*\}\s*\n", src, re.S)
    decls = re.findall(r"uniform\s+(\w+)\s+(\w+)\s*;", frag)
    names = sorted(set(n for _, n in decls))
    types = {n: t for t, n in decls}
    result[name] = {
        "vert": vert.strip("\n"),
        "frag": frag.strip("\n"),
        "glsl3": frag.lstrip().startswith("#version 300 es"),
        "uniformNames": names,
        "uniformTypes": types,
        "uniformsRaw": (uni.group(1).strip()[:900] if uni else ""),
    }
    print(f"{name}: glsl3={result[name]['glsl3']} uniforms={names}")

OUT.parent.mkdir(exist_ok=True)
OUT.write_text(json.dumps(result, indent=1), encoding="utf-8")
print(f"\n{len(result)} Shader -> {OUT}, {OUT.stat().st_size // 1024} KB")
