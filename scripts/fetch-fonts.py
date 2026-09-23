#!/usr/bin/env python3
"""Laedt die Google Fonts einmalig herunter, damit die Seite sie selbst ausliefert.

    python3 scripts/fetch-fonts.py

Ergebnis: img2/fonts/*.woff2 plus img2/fonts/fonts.css
Grund: ein Aufruf bei fonts.googleapis.com uebertraegt die IP des Besuchers an
Google. Selbst ausliefern spart die Einwilligung und ist schneller.
"""
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "img2" / "fonts"
OUT.mkdir(parents=True, exist_ok=True)

CSS_URL = ("https://fonts.googleapis.com/css2?"
           "family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,600;12..96,700;12..96,800"
           "&family=Karla:wght@400;500;600;700&display=swap")
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/124.0 Safari/537.36")


def get(url, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=40) as r:
        data = r.read()
    return data if binary else data.decode("utf-8")


css = get(CSS_URL)
# Nur die lateinischen Schnitte behalten, der Rest waere toter Ballast
blocks = re.findall(r"/\*\s*([\w\-\[\]]+)\s*\*/\s*(@font-face\s*\{.*?\})", css, re.S)
keep = [(name, block) for name, block in blocks if name in ("latin", "latin-ext")]
print(f"{len(blocks)} Schnitte geladen, {len(keep)} davon lateinisch")

out_css = []
seen = {}
for name, block in keep:
    url = re.search(r"url\((https://[^)]+\.woff2)\)", block).group(1)
    fam = re.search(r"font-family:\s*'([^']+)'", block).group(1)
    wght = re.search(r"font-weight:\s*([^;]+);", block).group(1).strip()
    fname = (fam.replace(" ", "") + "-" + wght.replace(" ", "_") + "-" + name + ".woff2")
    if url not in seen:
        (OUT / fname).write_bytes(get(url, binary=True))
        seen[url] = fname
    out_css.append(block.replace(url, "assets/fonts/" + seen[url]))

(OUT / "fonts.css").write_text("\n".join(out_css) + "\n", encoding="utf-8")
total = sum(f.stat().st_size for f in OUT.glob("*.woff2"))
print(f"{len(list(OUT.glob('*.woff2')))} Dateien, {total // 1024} KB -> img2/fonts/")
