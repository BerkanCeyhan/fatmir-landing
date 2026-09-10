#!/usr/bin/env python3
"""Fasst Shader und Uniform-Vorgaben zu einem JS-Objekt fuer die Seite zusammen.

    python3 scripts/build-bg-shaders.py

Schreibt gen/bg-shaders.js mit `const BG_SHADERS = {...};`
Rollen der Uniforms: time | resolution | mouse | interactive | color | literal.
"""
import json
import re
from pathlib import Path

shaders = json.loads(Path("gen/shaders.json").read_text(encoding="utf-8"))
config = json.loads(Path("gen/shader-config.json").read_text(encoding="utf-8"))

COLOR_HINT = re.compile(r"color|ubase|ulow|umid|uhigh", re.I)
INTERACT_HINT = re.compile(r"mouseinteract|enablemouse|mouseenabled|mouseactive", re.I)
LIGHT_HINT = re.compile(r"lightmode", re.I)

FALLBACK = {
    "uUseCustomColor": 1.0, "uDirection": 1.0, "uStepScale": 1.0,
    "uSpeed": 0.4, "uRotation": 0.0, "uCenterOffset": [0.0, 0.0],
}

out = {}
for name, data in shaders.items():
    types = data.get("uniformTypes", {})
    frag = data["frag"]
    rows = []
    color_index = 0
    for row in config[name]["uniforms"]:
        uni = row["uniform"]
        kind = row["kind"]
        gtype = types.get(uni)
        if gtype is None and re.search(r"uniform\s+vec3\s+" + re.escape(uni) + r"\s*\[", frag):
            gtype = "vec3[]"
        if kind == "todo":
            if LIGHT_HINT.search(uni):
                rows.append({"u": uni, "k": "literal", "v": 1.0})
                continue
            if INTERACT_HINT.search(uni):
                rows.append({"u": uni, "k": "interactive"})
                continue
            if COLOR_HINT.search(uni) or gtype == "vec3[]":
                rows.append({"u": uni, "k": "color", "i": color_index, "t": gtype or "vec3"})
                color_index += 1
                continue
            if uni in FALLBACK:
                rows.append({"u": uni, "k": "literal", "v": FALLBACK[uni]})
                continue
            rows.append({"u": uni, "k": "literal", "v": 0.0})
            continue
        if kind == "literal" and INTERACT_HINT.search(uni):
            rows.append({"u": uni, "k": "interactive"})
            continue
        if kind == "literal" and LIGHT_HINT.search(uni):
            rows.append({"u": uni, "k": "literal", "v": 1.0})
            continue
        if kind == "literal" and COLOR_HINT.search(uni):
            rows.append({"u": uni, "k": "color", "i": color_index, "t": gtype or "vec3"})
            color_index += 1
            continue
        if kind in ("time", "resolution", "mouse"):
            rows.append({"u": uni, "k": kind, "t": gtype or "vec2"})
            continue
        rows.append({"u": uni, "k": "literal", "v": row.get("value", 0.0)})
    out[name] = {"glsl3": data["glsl3"], "vert": data["vert"], "frag": frag, "uniforms": rows}

js = "const BG_SHADERS = " + json.dumps(out, ensure_ascii=False) + ";\n"
Path("gen/bg-shaders.js").write_text(js, encoding="utf-8")
print(f"{len(out)} Shader -> gen/bg-shaders.js, {len(js)//1024} KB")
for name, cfg in out.items():
    kinds = {}
    for r in cfg["uniforms"]:
        kinds[r["k"]] = kinds.get(r["k"], 0) + 1
    print(f"  {name}: {kinds}")
