#!/usr/bin/env python3
"""Baut aus den React-Bits-Quellen die Uniform-Vorgaben je Hintergrund.

    python3 scripts/shader-config.py

Liest /tmp/rb-<Name>.jsx plus gen/shaders.json und schreibt gen/shader-config.json:
je Shader eine Liste {uniform, kind, value}. kind ist einer von
literal | time | resolution | mouse | color | todo.
"""
import json
import re
from pathlib import Path

shaders = json.loads(Path("gen/shaders.json").read_text(encoding="utf-8"))
out = {}

TIME = {"utime", "itime", "time"}
RES = {"uresolution", "iresolution", "resolution"}
MOUSE = {"umouse", "imouse", "mouse", "mouseposition"}


def parse_props(src):
    """Default-Werte aus der Destrukturierung der Komponenten-Signatur."""
    patterns = [
        r"=\s*\(\{(.*?)\}\)\s*=>",          # const X = ({ a = 1 }) =>
        r"function\s+\w+\s*\(\{(.*?)\}\)",  # function X({ a = 1 })
        r"const\s*\{(.*?)\}\s*=\s*props\s*;",  # const { a = 1 } = props;
    ]
    body = ""
    for pat in patterns:
        for m in re.finditer(pat, src, re.S):
            if "=" in m.group(1):
                body += "," + m.group(1)
    if not body:
        return {}
    props = {}
    depth = 0
    token = ""
    parts = []
    for ch in body:
        if ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append(token)
            token = ""
        else:
            token += ch
    parts.append(token)
    for part in parts:
        if "=" not in part:
            continue
        key, val = part.split("=", 1)
        props[key.strip()] = val.strip()
    return props


for name, data in shaders.items():
    src = Path(f"/tmp/rb-{name}.jsx").read_text(encoding="utf-8")
    props = parse_props(src)
    entries = re.findall(r"(\w+)\s*:\s*\{\s*value:\s*([^\n]+?)\s*\}", data["uniformsRaw"])
    rows = []
    for uni, expr in entries:
        low = uni.lower()
        expr = expr.rstrip(",")
        if low in TIME:
            rows.append({"uniform": uni, "kind": "time"})
            continue
        if low in RES:
            rows.append({"uniform": uni, "kind": "resolution"})
            continue
        if low in MOUSE:
            rows.append({"uniform": uni, "kind": "mouse"})
            continue
        raw = props.get(expr, expr)
        if re.fullmatch(r"-?\d+(\.\d+)?", raw):
            rows.append({"uniform": uni, "kind": "literal", "value": float(raw)})
        elif raw in ("true", "false"):
            rows.append({"uniform": uni, "kind": "literal", "value": 1.0 if raw == "true" else 0.0})
        elif re.fullmatch(r"\[[\d\s.,\-]+\]", raw):
            rows.append({"uniform": uni, "kind": "literal", "value": json.loads(raw)})
        else:
            rows.append({"uniform": uni, "kind": "todo", "expr": raw[:60]})
    out[name] = {"glsl3": data["glsl3"], "uniforms": rows}
    todo = [r["uniform"] + "=" + r.get("expr", "") for r in rows if r["kind"] == "todo"]
    print(f"{name}: {len(rows)} Uniforms, offen: {todo if todo else 'keine'}")

Path("gen/shader-config.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
print("\n-> gen/shader-config.json")
